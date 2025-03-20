from typing import List, Literal
from .utils import format_base_url
from .api_client import ApiClient


class UnifiedCatalogClient:
    """
    Microsoft Purview Unified Catalog client for interacting with the Unified Catalog API.
    """

    def __init__(self, account_id: str, credential: any):
        """
        Initialize the Microsoft Purview Unified Catalog client.

        :param account_id: The guid of the Microsoft Purview account.
        :param credential: The azure.identity credential used to authenticate requests.
        """
        self.account_id = account_id
        self.credential = credential
        self.api_client = ApiClient(format_base_url(account_id), credential)

    def get_governance_domains(self):
        """
        Get the list of governance domains.

        :return: List of governance domains.
        """

        response = self.api_client.get("/businessdomains")
        return response.data["value"]

    def get_governance_domain_by_id(self, domain_id: str):
        """
        Get a governance domain by its ID.

        :param domain_id: The ID of the governance domain.
        :return: The governance domain data.
        """
        response = self.api_client.get(f"/businessdomains/{domain_id}")
        return response.data

    GovernanceDomainType = Literal[
        "FunctionalUnit", "LineOfBusiness", "DataDomain", "Regulatory", "Project"
    ]

    GovernanceDomainStatus = Literal["Draft", "Published"]

    def create_governance_domain(
        self,
        name: str,
        description: str,
        type: GovernanceDomainType,
        parent_id: str = None,
        status: GovernanceDomainStatus = "Draft",
    ):
        """
        Create a new governance domain.

        :param name: The name of the governance domain.
        :param description: The description of the governance domain.
        :param type: The type of the governance domain.
        :param parent_id: Optional ID of the parent governance domain.
        :param status: Optional status of the governance domain.
        :return: The created governance domain.
        """

        data = {
            "name": name,
            "description": description,
            "type": type,
            "parent_id": parent_id,
            "status": status,
        }
        response = self.api_client.post("/businessdomains", data=data)
        return response.data

    def update_governance_domain(
        self,
        governance_domain_id: str,
        name: str = None,
        description: str = None,
        type: str = None,
        parent_id: str = None,
        owners: List[dict] = [],
        status: GovernanceDomainStatus = "Draft",
    ):
        data = {
            "id": governance_domain_id,
            "name": name,
            "description": description,
            "type": type,
            "parent_id": parent_id,
            "contacts": {"owner": [{"id": owner["id"]} for owner in owners]},
            "status": status,
        }

        try:
            response = self.api_client.put(
                f"/businessdomains/{governance_domain_id}", data=data
            )
            return response.data
        except Exception as e:
            raise Exception(e)

    def delete_governance_domain(self, domain_id: str):
        """
        Delete a governance domain.

        :param domain_id: The ID of the governance domain to delete.
        :return: The response from the API.
        """

        try:
            response = self.api_client.delete(f"/businessdomains/{domain_id}")
            if not response.status_code == 204:
                return False
            return True
        except Exception as e:
            raise Exception(e)

    TermStatus = Literal["Draft", "Published", "Expired"]

    def get_terms(self, governance_domain_id: str):
        """
        Get the list of terms.

        :return: List of terms.
        """
        response = self.api_client.get(f"/terms?domainId={governance_domain_id}")
        return response.data["value"]

    def create_term(
        self,
        name: str,
        description: str,
        governance_domain_id: str,
        parent_id: str = None,
        owners: List[dict] = [],
        acronyms: List[str] = [],
        resources: List[dict] = [],
        status: TermStatus = "Draft",
    ):
        """
        Create a new term.

        :param name: The name of the term.
        :param description: The description of the term.
        :param governance_domain_id: The ID of the governance domain.
        :param parent_id: Optional ID of the parent term.
        :param owners: Optional ids of the owners of the term.
        :param status: Optional status of the term.
        :param acronyms: Optional list of acronyms for the term. Each acronym should be a dictionary with 'name' and 'url' keys.
        :param resources: Optional list of resources for the term. Each resource should be a dictionary with 'name' and 'url' keys.
        :return: The created term.
        """

        data = {
            "name": name,
            "description": description,
            "domain": governance_domain_id,
            "parent_id": parent_id,
            "contacts": {"owner": [{"id": owner["id"]} for owner in owners]},
            "acronyms": acronyms,
            "resources": [
                {"name": resource["name"], "url": resource["url"]}
                for resource in resources
            ],
            "status": status,
        }
        print(data)
        response = self.api_client.post("/terms", data=data)
        return response.data

    def update_term(
        self,
        term_id: str,
        name: str = None,
        description: str = None,
        governance_domain_id: str = None,
        parent_id: str = None,
        owners: List[dict] = [],
        acronyms: List[str] = [],
        resources: List[dict] = [],
        status: TermStatus = "Draft",
    ):
        """
        Update an existing term.

        :param term_id: The ID of the term to update.
        :param name: The new name of the term.
        :param description: The new description of the term.
        :param governance_domain_id: The new ID of the governance domain.
        :param parent_id: Optional new ID of the parent term.
        :param owners: Optional new ids of the owners of the term.
        :param status: Optional new status of the term.
        :param acronyms: Optional new list of acronyms for the term. Each acronym should be a dictionary with 'name' and 'url' keys.
        :param resources: Optional new list of resources for the term. Each resource should be a dictionary with 'name' and 'url' keys.
        :return: The updated term.
        """

        data = {
            "id": term_id,
            "name": name,
            "description": description,
            "domain": governance_domain_id,
            "parent_id": parent_id,
            "contacts": {"owner": [{"id": owner["id"]} for owner in owners]},
            "acronyms": acronyms,
            "resources": [
                {"name": resource["name"], "url": resource["url"]}
                for resource in resources
            ],
            "status": status,
        }

        response = self.api_client.put(f"/terms/{term_id}", data=data)
        return response.data

    def delete_term(self, term_id: str):
        """
        Delete a term.

        :param term_id: The ID of the term to delete.
        :return: The response from the API.
        """
        try:
            response = self.api_client.delete(f"/terms/{term_id}")
            if not response.status_code == 204:
                return False
            return True
        except Exception as e:
            raise Exception(e)

    def get_term_by_id(self, term_id: str):
        """
        Get a term by its ID.

        :param term_id: The ID of the term.
        :return: The term data.
        """
        response = self.api_client.get(f"/terms/{term_id}")
        return response.data

    RelationshipType = Literal["Synonym", "Related"]
    RelationshipEntityType = Literal[
        "Term", "DataProduct", "CriticalDataElement", "CustomMetadata"
    ]

    def create_relationship(
        self,
        entity_type: RelationshipEntityType,
        entity_id: str,
        relationship_type: RelationshipType,
        target_entity_id: str,
        description: str = "",
    ):
        """
        Create a relationship between entities.

        :param entity_type: The type of the entity (Term, DataProduct, CriticalDataElement).
        :param entity_id: The ID of the entity to create the relationship for.
        :param relationship_type: The type of the relationship (Synonym or Related).
        :param target_entity_id: The ID of the target entity to create the relationship with.
        :param description: Optional description of the relationship.
        :return: The created relationship.
        """

        endpoint_map = {
            "Term": "terms",
            "DataProduct": "dataproducts",
            "CriticalDataElement": "criticalDataElements",
        }

        if entity_type not in endpoint_map:
            raise ValueError(f"Unsupported entity type: {entity_type}")

        endpoint = f"/{endpoint_map[entity_type]}/{entity_id}/relationships"
        data = {
            "description": description,
            "entityId": target_entity_id,
            "relationshipType": relationship_type,
        }
        params = {
            "entityType": entity_type,
        }
        response = self.api_client.post(endpoint, data=data, params=params)
        return response.data

    def delete_relationship(
        self,
        entity_type: RelationshipEntityType,
        entity_id: str,
        target_entity_id: str,
        relationship_type: RelationshipType,
    ):
        """
        Delete a relationship between entities.

        :param entity_type: The type of the entity (Term, DataProduct, CriticalDataElement).
        :param entity_id: The ID of the entity to delete the relationship from.
        :param target_entity_id: The ID of the related entity.
        :param relationship_type: The type of the relationship (Synonym or Related).
        :return: The response from the API.
        """

        endpoint_map = {
            "Term": "terms",
            "DataProduct": "dataproducts",
            "CriticalDataElement": "criticalDataElements",
        }

        if entity_type not in endpoint_map:
            raise ValueError(f"Unsupported entity type: {entity_type}")

        endpoint = f"/{endpoint_map[entity_type]}/{entity_id}/relationships"
        params = {
            "entityId": target_entity_id,
            "entityType": entity_type,
            "relationshipType": relationship_type,
        }
        response = self.api_client.delete(endpoint, params=params)
        if response.status_code != 204:
            return False
        return True

    # def create_term_relationship(
    #     self,
    #     term_id: str,
    #     relationship_type: RelationshipType,
    #     entity_id: str,
    #     description: str = "",
    # ):
    #     """
    #     Create a relationship between two terms.

    #     :param term_id: The ID of the term to create the relationship for.
    #     :param relationship_type: The type of the relationship (Synonym or Related).
    #     :param entity_id: The ID of the target entity to create the relationship with.
    #     :param description: Optional description of the relationship.
    #     :return: The created relationship.
    #     """

    #     data = {
    #         "description": description,
    #         "entityId": entity_id,
    #         "relationshipType": relationship_type,
    #     }
    #     response = self.api_client.post(f"/terms/{term_id}/relationships", data=data)
    #     return response.data

    # def delete_term_relationship(
    #     self,
    #     term_id: str,
    #     entity_id: str,
    #     entity_type: RelationshipEntityType,
    #     relationship_type: RelationshipType,
    # ):
    #     """
    #     Delete a relationship between two terms.

    #     :param term_id: The ID of the term to delete the relationship from.
    #     :param entity_id: The ID of the related entity.
    #     :param relationship_type: The type of the relationship (Synonym or Related).
    #     :return: The response from the API.
    #     """

    #     try:
    #         response = self.api_client.delete(
    #             f"/terms/{term_id}/relationships?entityId={entity_id}&entityType={entity_type}&relationshipType={relationship_type}"
    #         )
    #         if not response.status_code == 204:
    #             return False
    #         return True
    #     except Exception as e:
    #         raise Exception(e)

    # Data Products
    DataProductStatus = Literal["Draft", "Published", "Expired"]
    DataProductType = Literal[
        "Dataset",
        "MasterDataAndReferenceData",
        "BusinessSystemOrApplication",
        "ModelTypes",
        "DashboardsOrReports",
        "Operational",
    ]
    DataProductUpdateFrequency = Literal[
        "Hourly", "Daily", "Weekly", "Monthly", "Quarterly", "Yearly"
    ]

    def get_data_products(self, governance_domain_id: str):
        """
        Get the list of data products."
        :param governance_domain_id: The ID of the governance domain."
        :return: List of data products.
        """

        response = self.api_client.get(f"/dataproducts?domainId={governance_domain_id}")
        return response.data["value"]

    def get_data_product_by_id(self, data_product_id: str):
        """
        Get a data product by its ID.

        :param data_product_id: The ID of the data product.
        :return: The data product data.
        """

        response = self.api_client.get(f"/dataproducts/{data_product_id}")
        return response.data

    def create_data_product(
        self,
        name: str,
        description: str,
        governance_domain_id: str,
        type: DataProductType,
        business_use: str,
        owners: List[dict] = [],
        audience: List[str] = [],
        terms_of_use: List[str] = [],
        documentation: List[str] = [],
        updateFrequency: DataProductUpdateFrequency = None,
        status: DataProductStatus = "Draft",
        endorsed: bool = False,
    ):
        """
        Create a new data product.

        :param name: The name of the data product.
        :param description: The description of the data product.
        :param governance_domain_id: The ID of the governance domain.
        :param type: The type of the data product.
        :param business_use: The business use of the data product.
        :param owners: Optional ids of the owners of the data product.
        :param audience: Optional list of audience for the data product.
        :param terms_of_use: Optional list of terms of use for the data product.
        :param documentation: Optional list of documentation for the data product.
        :param updateFrequency: Optional update frequency of the data product.
        :param status: Optional status of the data product.
        :param endorsed: Optional boolean indicating if the data product is endorsed.
        :return: The created data product.
        """

        data = {
            "name": name,
            "description": description,
            "domain": governance_domain_id,
            "type": type,
            "businessUse": business_use,
            "contacts": {
                "owner": [
                    {"id": owner["id"], "description": owner.get("description", "")}
                    for owner in owners
                ]
            },
            "audience": audience,
            "termsOfUse": terms_of_use,
            "documentation": documentation,
            "updateFrequency": updateFrequency,
            "status": status,
            "endorsed": endorsed,
        }
        response = self.api_client.post("/dataproducts", data=data)
        return response.data

    def update_data_product(
        self,
        data_product_id: str,
        name: str = None,
        description: str = None,
        governance_domain_id: str = None,
        type: str = None,
        business_use: str = None,
        owners: List[dict] = [],
        audience: List[str] = [],
        terms_of_use: List[str] = [],
        documentation: List[str] = [],
        updateFrequency: DataProductUpdateFrequency = None,
        status: DataProductStatus = "Draft",
        endorsed: bool = False,
    ):
        """
        Update an existing data product.
        :param data_product_id: The ID of the data product to update.
        :param name: The new name of the data product.
        :param description: The new description of the data product.
        :param governance_domain_id: The new ID of the governance domain.
        :param type: The new type of the data product.
        :param business_use: The new business use of the data product.
        :param owners: Optional new ids of the owners of the data product.
        :param audience: Optional new list of audience for the data product.
        :param terms_of_use: Optional new list of terms of use for the data product.
        :param documentation: Optional new list of documentation for the data product.
        :param updateFrequency: Optional new update frequency of the data product.
        :param status: Optional new status of the data product.
        :param endorsed: Optional new boolean indicating if the data product is endorsed.
        :return: The updated data product.
        """
        data = {
            "id": data_product_id,
            "name": name,
            "description": description,
            "domain": governance_domain_id,
            "type": type,
            "businessUse": business_use,
            "contacts": {
                "owner": [
                    {"id": owner["id"], "description": owner.get("description", "")}
                    for owner in owners
                ]
            },
            "audience": audience,
            "termsOfUse": terms_of_use,
            "documentation": documentation,
            "updateFrequency": updateFrequency,
            "status": status,
            "endorsed": endorsed,
        }

        response = self.api_client.put(f"/dataproducts/{data_product_id}", data=data)
        return response.data

    def delete_data_product(self, data_product_id: str):
        """
        Delete a data product.

        :param data_product_id: The ID of the data product to delete.
        :return: The response from the API.
        """

        try:
            response = self.api_client.delete(f"/dataproducts/{data_product_id}")
            if not response.status_code == 204:
                return False
            return True
        except Exception as e:
            raise Exception(e)

    # TODO: Data Product Term Relationship (Create, Delete)
    # Create: dataproducts/<data-product-id>/relationships?entityType=Term
    # {"entityId":"94e22736-067d-4283-9806-1efdbac07297","description":"Test Term Description","relationshipType":"Related"}
    # Delete: dataproducts/58ddd299-5434-493b-956f-01c76171621f/relationships?entityType=Term&entityId=4939d006-fff0-4bad-9b03-53700b48b31b&relationshipType=Related

    # Objectives
    ObjectiveStatus = Literal["Draft", "Published", "Closed"]

    def create_objective(
        self,
        definition: str,
        governance_domain_id: str,
        owners: List[dict] = [],
        status: ObjectiveStatus = "Draft",
        target_date: str = None,
    ):
        """
        Create a new objective.

        :param definition: Definition of the objective.
        :param governance_domain_id: The ID of the governance domain.
        :param owners: Optional ids of the owners of the objective.
        :param status: Optional status of the objective.
        :param target_date: Optional target date of the objective. Eg: "2025-01-01T00:00:00Z"
        :return: The created objective.
        """

        data = {
            "domain": governance_domain_id,
            "contacts": {
                "owner": [
                    {"id": owner["id"], "description": owner.get("description", "")}
                    for owner in owners
                ]
            },
            "status": status,
            "definition": definition,
            "targetDate": target_date,
        }
        response = self.api_client.post("/objectives", data=data)
        return response.data

    def get_objectives(self, governance_domain_id: str):
        """
        Get the list of objectives.

        :param governance_domain_id: The ID of the governance domain.
        :return: List of objectives.
        """

        response = self.api_client.get(f"/objectives?domainId={governance_domain_id}")
        return response.data["value"]

    def get_objective_by_id(self, objective_id: str):
        """
        Get an objective by its ID.

        :param objective_id: The ID of the objective.
        :return: The objective data.
        """

        response = self.api_client.get(f"/objectives/{objective_id}")
        return response.data

    def update_objective(
        self,
        objective_id: str,
        definition: str = None,
        governance_domain_id: str = None,
        owners: List[dict] = [],
        status: ObjectiveStatus = "Draft",
        target_date: str = None,
    ):
        """
        Update an existing objective.

        :param objective_id: The ID of the objective to update.
        :param definition: The new definition of the objective.
        :param governance_domain_id: The new ID of the governance domain.
        :param owners: Optional new ids of the owners of the objective.
        :param status: Optional new status of the objective.
        :param target_date: Optional new target date of the objective. Eg: "2025-01-01T00:00:00Z"
        :return: The updated objective.
        """

        data = {
            "id": objective_id,
            "domain": governance_domain_id,
            "contacts": {
                "owner": [
                    {"id": owner["id"], "description": owner.get("description", "")}
                    for owner in owners
                ]
            },
            "status": status,
            "definition": definition,
            "targetDate": target_date,
        }

        response = self.api_client.put(f"/objectives/{objective_id}", data=data)
        return response.data

    def delete_objective(self, objective_id: str):
        """
        Delete an objective.

        :param objective_id: The ID of the objective to delete.
        :return: The response from the API.
        """

        try:
            response = self.api_client.delete(f"/objectives/{objective_id}")
            if not response.status_code == 204:
                return False
            return True
        except Exception as e:
            raise Exception(e)

    # Critical Data Elements
    CriticalDataElementStatus = Literal["Draft", "Published", "Expired"]

    def create_critical_data_element(
        self,
        name: str,
        description: str,
        governance_domain_id: str,
        owners: List[dict] = [],
        status: CriticalDataElementStatus = "Draft",
        data_type: str = "Number",
    ):
        """
        Create a new critical data element.

        :param name: The name of the critical data element.
        :param description: The description of the critical data element.
        :param governance_domain_id: The ID of the governance domain.
        :param owners: Optional ids of the owners of the critical data element.
        :param status: Optional status of the critical data element.
        :param data_type: The data type of the critical data element.
        :return: The created critical data element.
        """

        data = {
            "name": name,
            "description": description,
            "domain": governance_domain_id,
            "contacts": {
                "owner": [
                    {"id": owner["id"], "description": owner.get("description", "")}
                    for owner in owners
                ]
            },
            "status": status,
            "dataType": data_type,
        }
        response = self.api_client.post("/criticalDataElements", data=data)
        return response.data

    def get_critical_data_elements(self, governance_domain_id: str):
        """
        Get the list of critical data elements.

        :param governance_domain_id: The ID of the governance domain.
        :return: List of critical data elements.
        """
        response = self.api_client.get(
            f"/criticalDataElements?domainId={governance_domain_id}"
        )
        return response.data["value"]

    def get_critical_data_element_by_id(self, cde_id: str):
        """
        Get a critical data element by its ID.

        :param cde_id: The ID of the critical data element.
        :return: The critical data element data.
        """

        response = self.api_client.get(f"/criticalDataElements/{cde_id}")
        return response.data

    def update_critical_data_element(
        self,
        cde_id: str,
        name: str = None,
        description: str = None,
        governance_domain_id: str = None,
        owners: List[dict] = [],
        status: CriticalDataElementStatus = "Draft",
        data_type: str = "Number",
    ):
        """
        Update an existing critical data element.

        :param cde_id: The ID of the critical data element to update.
        :param name: The new name of the critical data element.
        :param description: The new description of the critical data element.
        :param governance_domain_id: The new ID of the governance domain.
        :param owners: Optional new ids of the owners of the critical data element.
        :param status: Optional new status of the critical data element.
        :param data_type: The new data type of the critical data element.
        :return: The updated critical data element.
        """

        data = {
            "id": cde_id,
            "domain": governance_domain_id,
            "contacts": {
                "owner": [
                    {"id": owner["id"], "description": owner.get("description", "")}
                    for owner in owners
                ]
            },
            "status": status,
            "name": name,
            "description": description,
            "dataType": data_type,
        }

        response = self.api_client.put(f"/criticalDataElements/{cde_id}", data=data)
        return response.data

    def delete_critical_data_element(self, cde_id: str):
        """
        Delete a critical data element.

        :param cde_id: The ID of the critical data element to delete.
        :return: The response from the API.
        """

        try:
            response = self.api_client.delete(f"/criticalDataElements/{cde_id}")
            if not response.status_code == 204:
                return False
            return True
        except Exception as e:
            raise Exception(e)

    # Key Results
    KeyResultStatus = Literal["Behind", "OnTrack", "AtRisk"]

    def create_key_result(
        self,
        progress: int,
        goal: int,
        max: int,
        status: KeyResultStatus,
        definition: str,
        objective_id: str,
        governance_domain_id: str,
    ):
        """
        Create a new key result.

        :param progress: The progress of the key result.
        :param goal: The goal of the key result.
        :param max: The maximum value of the key result.
        :param status: The status of the key result.
        :param definition: The definition of the key result.
        :param objective_id: The ID of the objective.
        :param governance_domain_id: The ID of the governance domain.
        :return: The created key result.
        :raises ValueError: If progress, goal, or max are negative integers.
        """

        if progress < 0 or goal < 0 or max <= 0:
            raise ValueError(
                "Progress and goal must be zero (0) or positive integers, max must be a positive integer."
            )

        data = {
            "progress": progress,
            "goal": goal,
            "max": max,
            "status": status,
            "definition": definition,
            "domainId": governance_domain_id,
        }
        response = self.api_client.post(
            f"/objectives/{objective_id}/keyResults", data=data
        )
        return response.data

    def update_key_result(
        self,
        key_result_id: str,
        objective_id: str,
        governance_domain_id: str,
        progress: int = None,
        goal: int = None,
        max: int = None,
        status: KeyResultStatus = None,
        definition: str = None,
    ):
        """
        Update an existing key result.

        :param key_result_id: The ID of the key result to update.
        :param objective_id: The ID of the objective.
        :param governance_domain_id: The ID of the governance domain.
        :param progress: The new progress of the key result.
        :param goal: The new goal of the key result.
        :param max: The new maximum value of the key result.
        :param status: The new status of the key result.
        :param definition: The new definition of the key result.
        :return: The updated key result.
        :raises ValueError: If progress, goal, or max are negative integers.
        """

        if progress < 0 or goal < 0 or max <= 0:
            raise ValueError(
                "Progress and goal must be zero (0) or positive integers, max must be a positive integer."
            )

        data = {
            "id": key_result_id,
            "progress": progress,
            "goal": goal,
            "max": max,
            "status": status,
            "definition": definition,
            "domainId": governance_domain_id,
        }

        response = self.api_client.put(
            f"/objectives/{objective_id}/keyResults/{key_result_id}", data=data
        )
        return response.data

    def delete_key_result(self, key_result_id: str, objective_id: str):
        """
        Delete a key result.

        :param key_result_id: The ID of the key result to delete.
        :param objective_id: The ID of the objective.
        :return: The response from the API.
        """

        try:
            response = self.api_client.delete(
                f"/objectives/{objective_id}/keyResults/{key_result_id}"
            )
            if not response.status_code == 204:
                return False
            return True
        except Exception as e:
            raise Exception(e)

    def get_key_results(self, objective_id: str):
        """
        Get the list of key results for an objective.

        :param objective_id: The ID of the objective.
        :return: List of key results.
        """

        response = self.api_client.get(f"/objectives/{objective_id}/keyResults")
        return response.data["value"]

    def get_key_result_by_id(self, key_result_id: str, objective_id: str):
        """
        Get a key result by its ID.

        :param key_result_id: The ID of the key result.
        :param
        objective_id: The ID of the objective.
        :return: The key result data.
        """
        response = self.api_client.get(
            f"/objectives/{objective_id}/keyResults/{key_result_id}"
        )
        return response.data
