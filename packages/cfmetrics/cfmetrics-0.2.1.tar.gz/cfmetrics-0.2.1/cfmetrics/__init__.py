import os
import requests
from datetime import datetime, timedelta
from cfmetrics import query, data_format

class Config:

    def __init__(self):
        self.cf_graphql_url="https://api.cloudflare.com/client/v4/graphql"
        self.cf_api_url="https://api.cloudflare.com/client/v4"

    def get_url(self):
        return self.cf_graphql_url, self.cf_api_url

class Auth:

    def __init__(self, api_key: str, api_key_email: str):
        if not api_key or not api_key_email:
            raise ValueError("Cloudflare Account ID, Zone ID, API Key, API Key Email is required")

        self.api_key=api_key
        self.api_key_email=api_key_email
        self.headers={
                "Authorization": f"Bearer {self.api_key}",
                "X-AUTH-EMAIL": self.api_key_email
        }

    def Account(self, account_id: str):
        return Account(self.api_key, self.api_key_email, account_id)


class Account:

    def __init__(self, api_key: str, api_key_email: str, account_id: str):
        if not api_key or not api_key_email or not account_id:
            raise ValueError("Cloudflare API Key, Email API Key and Account ID is required")

        self.api_key=api_key
        self.api_key_email=api_key
        self.account_id=account_id
        self.cf_graphql_url, self.cf_api_url = Config().get_url()
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "X-AUTH-EMAIL": self.api_key_email
        }

    def Zone(self, zone_id: str):
        return Zone(self.api_key, self.api_key_email, self.account_id, zone_id)

class Zone:

    def __init__(self, api_key: str, api_key_email: str, account_id: str, zone_id: str):
        if not api_key or not api_key_email or not zone_id:
            raise ValueError("Cloudflare API Key, Email and Zone ID is required")

        self.api_key = api_key
        self.api_key_email = api_key_email
        self.account_id=account_id
        self.zone_id = zone_id
        self.cf_graphql_url, self.cf_api_url = Config().get_url()
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "X-AUTH-EMAIL": self.api_key_email
        }

    def get_dns_records(self):
        """
            Fetch DNS records for a given zone (A and CNAME records)
        """
        url = f"{self.cf_api_url}/zones/{self.zone_id}/dns_records"
        records = []

        for record_type in ["A", "CNAME"]:
            response = requests.get(url, headers=self.headers, params={"type": record_type})
            if response.status_code ==200:
                records.extend(response.json().get("result", []))
            else:
                print(f"Failed to fetch {record_type} records: {response.text}")

        return records

    def get_domain_plan(self):
        """
        Get the Domain Liecense or Pricing Plan so it will give a clue about which metric
        that we could actually scrape
        The License most likely FREE/PRO/BUSINESS/ENTERPRISE
        at this moment we only support FREE and BUSINESS
        Current Response
         1. Free Website
         2. Business Website
        """
    
        url = f"{self.cf_api_url}/zones/{self.zone_id}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            zone_info = response.json().get("result", {})
            plan_name = zone_info.get("plan", {}).get("name", "Unknown")
            return plan_name
        else:
            print(f"Failed to fetch plan details for zone {self.zone_id}:", response.text)
            return "Unknown"

    def get_traffics(self, start_datetime=(datetime.now()-timedelta(seconds=2764000)).strftime("%Y-%m-%dT%H:%M:%SZ"), end_datetime=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")):
        """
        This stupid feature already tested in Business Plan, its not working with Free plan
        and still not yet tested with Pro Plan
        """

        try:
            check_start_datetime = datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            raise ValueError("Invalid date format. Expected format: YYYY-MM-DDTHH:MM:SSZ")

        threshold_date = datetime.utcnow() - timedelta(seconds=2764800)

        if (threshold_date - check_start_datetime).total_seconds() > 2764800:
            raise ValueError(f"start_datetime cannot be more than 2,764,800 seconds (32 days) ago. Given: {start_datetime}")

        dns_records = [result['name'] for result in self.get_dns_records()]
        listofDomainFilter = []
        queryBody = {}

        if "Free Website" in self.get_domain_plan():
            raise ConnectionError(f"This Zone ID {self.zone_id} using Free Plan Pricing, Move to Business to use this feature")

        if "Business" in self.get_domain_plan():
            listofDomainFilter = [{"clientRequestHTTPHost": item} for item in dns_records]

            queryBody = {
                "query": """
                    query VisitsDaily($zoneTag: string, $filter: ZoneHttpRequestsAdaptiveGroupsFilter_InputObject){
                        viewer{
                            zones(filter: {zoneTag: $zoneTag}) {
                            series: httpRequestsAdaptiveGroups(limit: 10000, filter: $filter) {
                                count # pageview
                                avg {
                                    sampleInterval
                                    }
                                sum {
                                    edgeResponseBytes # data transfer
                                    visits # according to documentation this is the number of requests by end-users that were initiated from a different website. so its requests I guess.
                                     }
                                dimensions {
                                    host: clientRequestHTTPHost
                                    ts: date # datetimeFifteenMinutes
                                    }
                                }
                            }
                        }
                    }
                        """,
                "variables":{
                    "zoneTag": self.zone_id,
                    "filter": {
                        "AND": [{
                            "datetime_geq": start_datetime,
                            "datetime_leq": end_datetime
                        }, {
                            "requestSource": "eyeball"
                        }, {
                            "AND": [{
                                "edgeResponseStatus": 200,
                                "edgeResponseContentTypeName": "html"
                            }]
                        }, {
                            "OR": listofDomainFilter
                        }]
                    }
                }
            }

        getDataOK = requests.post(self.cf_graphql_url, headers=self.headers, json=queryBody)
        if getDataOK.status_code != 200:
            raise ConnectionError(f"Request to {getDataOK.url} got response {getDataOK.status_code} == {getDataOK.text}") 
        
        dataResult = getDataOK.json()
        if dataResult["data"] == None:
            raise ValueError(f"There is no data Response, maybe check the response {dataResult}")

        dataCompiled = {"by_date":{"date_lists": [], "dates": []}, "by_domain": {"domain_lists": [], "domains": []}}

        dataCompiled = data_format.model(getDataOK, "traffic")


        # somehow the value is always 0
        # will debug this later, will be disabled for a moment

        useFeatureError = False
        
        if useFeatureError:
            queryBody["variables"]["filter"]["AND"][2]["AND"][0]["edgeResponseStatus"] = 500
            getDataFailure = requests.post(self.cf_graphql_url, headers=self.headers, json=queryBody)
            
            if getDataFailure.status_code != 200:
                raise ConnectionError(f"Request to {getDataFailure.url} got response {getDataFailure.status_code} == {getDataFailure.text}") 
        
            dataResult = getDataFailure.json()

            if dataResult["data"] == None:
                raise ValueError(f"There is no data Response, maybe check the response {dataResult}")
            if getDataFailure.status_code != 200:
                return "ERROR to GET DATA FAILURE TRAFFIC"

            dataMetric = dataResult["data"]["viewer"]["zones"][0]["series"]
            for item in dataMetric:
                ts = item["dimensions"]["ts"]
                domainName = item["dimensions"]["host"]

                if ts in dataCompiled["by_date"]["date_lists"]:
                    currDateIndex = dataCompiled["by_date"]["date_lists"].index(ts)
                    currDomI = dataCompiled["by_date"]["dates"][currDateIndex]["domain_lists"].index(domainName)
                    dataCompiled["by_date"]["dates"][currDateIndex]["domains"][currDomI]["metrics"]["error_counts"] = item["count"]

                if domainName in dataCompiled["by_domain"]["domain_lists"]:
                    currDomI = dataCompiled["by_domain"]["domain_lists"].index(domainName)
                    currDateIndex = dataCompiled["by_domain"]["domains"][currDomI]["date_lists"].index(ts)
                    dataCompiled["by_domain"]["domains"][currDomI]["dates"][currDateIndex]["metrics"]["error_counts"] = item["count"] 

        return dataCompiled


    def get_web_analytics(self, start_date=(datetime.now()-timedelta(seconds=2764800)).strftime("%Y-%m-%dT%H:%M:%SZ"), end_date=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")):
        """
        This feature is available for any price plan
        """

        try:
            start_datetime = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            raise ValueError("Invalid date format. Expected format: YYYY-MM-DDTHH:MM:SSZ")


        dns_records = [result['name'] for result in self.get_dns_records()]
        listofDomainFilter = [{"requestHost": item} for item in dns_records]
        dataCompiled = {"by_date":{}, "by_domain": {}}
        queryBody = {
                "query": """
                    query RumDaily($accountTag: string, $filter: AccountRumPageloadEventsAdaptiveGroupsFilter_InputObject){
                        viewer{
                            accounts(filter: {accountTag: $accountTag}) {
                            series: rumPageloadEventsAdaptiveGroups(limit: 10000, filter: $filter) {
                                count # number of page viewed by end users
                                avg {
                                    sampleInterval
                                    }
                                sum {
                                    visits # according to documentation this is the number of requests by end-users that were initiated from a different website. so its requests I guess.
                                     }
                                dimensions {
                                    host: requestHost
                                    ts: date
                                    }
                                }
                            }
                        }
                    }
                        """,
                "variables":{
                    "accountTag": self.account_id,
                    "filter": {
                        "AND": [{
                            "datetime_geq": start_date,
                            "datetime_leq": end_date
                        }, {
                            "OR": listofDomainFilter
                        }]
                    }
                }
            }

        getDataOK = requests.post(self.cf_graphql_url, headers=self.headers, json=queryBody)
        if getDataOK.status_code != 200:
            raise ConnectionError(f"Request to {getDataOK.url} got response {getDataOK.status_code} == {getDataOK.text}") 
        
        dataResult = getDataOK.json()
        if dataResult["data"] == None:
            raise ValueError(f"There is no data Response, maybe check the response {dataResult}")
        

        dataCompiled = data_format.model(getDataOK, "rum")

        return dataCompiled

    def get_overview(self, start_date=(datetime.now()-timedelta(seconds=2764800)).strftime("%Y-%m-%d"), end_date=datetime.now().strftime("%Y-%m-%d")):

        try:
            start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Expected format: YYYY-MM-DD")

        queryBody = query.query_zone_overview(self.zone_id, start_date, end_date)
        
        getDataOK = requests.post(self.cf_graphql_url, headers=self.headers, json=queryBody)
        if getDataOK.status_code != 200:
            raise ConnectionError(f"Request to {getDataOK.url} got response {getDataOK.status_code} == {getDataOK.text}") 
        
        dataResult = getDataOK.json()
        if dataResult["data"] == None:
            raise ValueError(f"There is no data Response, maybe check the response {dataResult}")
        
        dataCompiled = {
            "totalUniqueUsers": {},
            "by_date": {
                "dates": [],
                "date_lists": []
            }
        }

        try:
            dataMetric = getDataOK.json()["data"]["viewer"]["zones"][0]
            dataCompiled["totalUniqueUsers"] = dataMetric["totals"][0]["uniq"]["uniques"]
            for item in dataMetric["zones"]:
                ts = item["dimensions"]["timeslot"]
                if ts not in dataCompiled["by_date"]["date_lists"]:
                    dataCompiled["by_date"]["dates"].append({
                        "date": ts,
                        "metrics": {
                            "browserMap": item["sum"]["browserMap"],
                            "bytes": item["sum"]["bytes"],
                            "cachedBytes": item["sum"]["cachedBytes"],
                            "cachedRequests": item["sum"]["cachedRequests"],
                            "contentTypeMap": item["sum"]["contentTypeMap"],
                            "countryMap": item["sum"]["countryMap"],
                            "pageViews": item["sum"]["pageViews"],
                            "requests": item["sum"]["requests"],
                            "responseStatusMap": item["sum"]["responseStatusMap"],
                            "threatPathingMap": item["sum"]["threatPathingMap"],
                            "threats": item["sum"]["threats"]
                        }
                    })
                    dataCompiled["by_date"]["date_lists"].append(ts)
        except (KeyError, IndexError, TypeError):
            return "Data is Missing or Invalid"

        return dataCompiled


