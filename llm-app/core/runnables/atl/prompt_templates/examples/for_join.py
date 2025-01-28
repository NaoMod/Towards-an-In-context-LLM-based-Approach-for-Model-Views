examples = [
{
"trans_desc": "The transformation will be used to migrate the infomation from the Company to the Corp.",
"ex_meta_1": 
"""
    @startuml
        title Company

        class Company {{
            +String name
        }}

        class Employee {{
            +String name
            +String position
        }}

        Company --> "0..*" Employee : employs

    @enduml
""",
"ex_meta_2": 
"""
    @startuml
        title Corp

        class Corporation {{
            +String corpName
        }}

        class Worker {{
            +String workerName
            +String jobTitle
        }}

        class Freelancer {{
            +String name
            +String task
        }}

        Corporation --> "0..*" Worker : hasWorkers

    @enduml
""",
"relations": 
"""
{{
    "relations": [
        {{
            "rule": "CompanyToCorporation",
            "from": {{
                "c": {{
                    "metamodel": "Company",
                    "class": "Company"
                }}
            }},
            "to": {{
                "corp": {{
                    "metamodel": "Corp",
                    "class": "Corporation"
                }},
            }}
        }},
        {{
            "rule": "EmployeeToWorker",
            "from": {{
                "e": {{
                    "metamodel": "Company",
                    "class": "Employee"
                }}
            }},
            "to": {{
                "w": {{
                    "metamodel": "Corp",
                    "class": "Worker",
                }},
                "f": {{
                    "metamodel": "Corp",
                    "class": "Freelancer",
                }}
            }}
        }}
    ]
}}
"""

},
{
        "trans_desc": "The transformation will convert a Library system to a Resource Management system.",
        "ex_meta_1": 
        """
            @startuml
                title Library

                class Library {{
                    +String libraryName
                }}

                class Book {{
                    +String title
                    +String author
                }}

                class Member {{
                    +String memberName
                    +String membershipDate
                }}

                Library --> "0..*" Book : contains
                Library --> "0..*" Member : serves

            @enduml
        """,
        "ex_meta_2": 
        """
            @startuml
                title Resource Management

                class ResourceCenter {{
                    +String centerName
                }}

                class Resource {{
                    +String resourceTitle
                    +String creator
                }}

                class User {{
                    +String userName
                    +String registrationDate
                }}

                ResourceCenter --> "0..*" Resource : manages
                ResourceCenter --> "0..*" User : registers

            @enduml
        """,
        "relations": 
        """
        {
            "relations": [
                {
                    "rule": "LibraryToResourceCenter",
                    "from": {
                        "l": {
                            "metamodel": "Library",
                            "class": "Library"
                        }
                    },
                    "to": {
                        "rc": {
                            "metamodel": "ResourceManagement",
                            "class": "ResourceCenter"
                        }
                    }
                },
                {
                    "rule": "BookToResource",
                    "from": {
                        "b": {
                            "metamodel": "Library",
                            "class": "Book"
                        }
                    },
                    "to": {
                        "r": {
                            "metamodel": "ResourceManagement",
                            "class": "Resource"
                        }
                    }
                },
                {
                    "rule": "MemberToUser",
                    "from": {
                        "m": {
                            "metamodel": "Library",
                            "class": "Member"
                        }
                    },
                    "to": {
                        "u": {
                            "metamodel": "ResourceManagement",
                            "class": "User"
                        }
                    }
                }
            ]
        }
        """
    },
    {
        "trans_desc": "The transformation will migrate the E-commerce system to a Supply Chain system.",
        "ex_meta_1": 
        """
            @startuml
                title E-commerce

                class Store {{
                    +String storeName
                }}

                class Product {{
                    +String productName
                    +double price
                }}

                class Customer {{
                    +String customerName
                    +String shippingAddress
                }}

                Store --> "0..*" Product : sells
                Store --> "0..*" Customer : serves

            @enduml
        """,
        "ex_meta_2": 
        """
            @startuml
                title Supply Chain

                class Warehouse {{
                    +String warehouseName
                }}

                class Item {{
                    +String itemName
                    +double cost
                }}

                class Distributor {{
                    +String distributorName
                    +String deliveryAddress
                }}

                Warehouse --> "0..*" Item : stores
                Warehouse --> "0..*" Distributor : supplies

            @enduml
        """,
        "relations": 
        """
        {
            "relations": [
                {
                    "rule": "StoreToWarehouse",
                    "from": {
                        "s": {
                            "metamodel": "Ecommerce",
                            "class": "Store"
                        }
                    },
                    "to": {
                        "w": {
                            "metamodel": "SupplyChain",
                            "class": "Warehouse"
                        }
                    }
                },
                {
                    "rule": "ProductToItem",
                    "from": {
                        "p": {
                            "metamodel": "Ecommerce",
                            "class": "Product"
                        }
                    },
                    "to": {
                        "i": {
                            "metamodel": "SupplyChain",
                            "class": "Item"
                        }
                    }
                },
                {
                    "rule": "CustomerToDistributor",
                    "from": {
                        "c": {
                            "metamodel": "Ecommerce",
                            "class": "Customer"
                        }
                    },
                    "to": {
                        "d": {
                            "metamodel": "SupplyChain",
                            "class": "Distributor"
                        }
                    }
                }
            ]
        }
        """
    },
    {
        "trans_desc": "The transformation will map the Hospital system to the Healthcare Network system.",
        "ex_meta_1": 
        """
            @startuml
                title Hospital

                class Hospital {{
                    +String hospitalName
                }}

                class Doctor {{
                    +String doctorName
                    +String specialty
                }}

                class Patient {{
                    +String patientName
                    +int patientAge
                }}

                Hospital --> "0..*" Doctor : employs
                Hospital --> "0..*" Patient : admits

            @enduml
        """,
        "ex_meta_2": 
        """
            @startuml
                title Healthcare Network

                class Clinic {{
                    +String clinicName
                }}

                class Practitioner {{
                    +String practitionerName
                    +String expertise
                }}

                class Client {{
                    +String clientName
                    +int age
                }}

                Clinic --> "0..*" Practitioner : hires
                Clinic --> "0..*" Client : services

            @enduml
        """,
        "relations": 
        """
        {
            "relations": [
                {
                    "rule": "HospitalToClinic",
                    "from": {
                        "h": {
                            "metamodel": "Hospital",
                            "class": "Hospital"
                        }
                    },
                    "to": {
                        "c": {
                            "metamodel": "HealthcareNetwork",
                            "class": "Clinic"
                        }
                    }
                },
                {
                    "rule": "DoctorToPractitioner",
                    "from": {
                        "d": {
                            "metamodel": "Hospital",
                            "class": "Doctor"
                        }
                    },
                    "to": {
                        "p": {
                            "metamodel": "HealthcareNetwork",
                            "class": "Practitioner"
                        }
                    }
                },
                {
                    "rule": "PatientToClient",
                    "from": {
                        "p": {
                            "metamodel": "Hospital",
                            "class": "Patient"
                        }
                    },
                    "to": {
                        "c": {
                            "metamodel": "HealthcareNetwork",
                            "class": "Client"
                        }
                    }
                }
            ]
        }
        """
    }
]