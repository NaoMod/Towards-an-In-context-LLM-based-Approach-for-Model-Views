examples = [
    {
"view_desc": "The view  should conatins the name, and email from the Customer and also the name of the item bought by they.",
"ex_meta_1":
"""
@startuml

    class Customer {{
        +int id
        +String name
        +String email
        +String deliveryAddress
    }}

    @enduml
""",
"ex_meta_2":
"""
@startuml

    class Item {{
        +int id
        +String name
        +String category
    }}

    class Order {{
        +int orderId
        +String orderNumber
        +Date orderDate
        +Date creationDate
        +String currentOrderStatus
        +String customerName
    }}

    @enduml
""",
"relations":
"""
{{
    "relations": [
        {{
            "name": "itemBoughtByCustomer",
            "classes": [
                "Customer",
                "Item"
            ]
        }}
    ]
}}
"""
},
{
"view_desc": "The view should display the name and department of an employee along with the project they are working on and the manager supervising the project.",
"ex_meta_1":
"""
@startuml

    class Employee {{
        +int id
        +String name
        +String department
        +String email
    }}

    class Manager {{
        +int id
        +String name
        +String department
        +String email
    }}

    @enduml
""",
"ex_meta_2":
"""
@startuml

    class Project {{
        +int id
        +String name
        +Date startDate
        +Date endDate
    }}

    class Assignment {{
        +int assignmentId
        +String role
        +String employeeName
    }}

    @enduml
""",
"relations":
"""
{{
    "relations": [
        {{
            "name": "employeeAssignedToProject",
            "classes": [
                "Employee",
                "Project"
            ]
        }},
        {{
            "name": "projectSupervisedByManager",
            "classes": [
                "Project",
                "Manager"
            ]
        }}
    ]
}}
"""
},
{
"view_desc": "The view should display the name and department of an employee along with the project they are working on and the manager supervising the project.",
"ex_meta_1":
"""
@startuml

    class Employee {{
        +int id
        +String name
        +String department
        +String email
    }}

    class Manager {{
        +int id
        +String name
        +String department
        +String email
    }}

    @enduml
""",
"ex_meta_2":
"""
@startuml

    class Project {{
        +int id
        +String name
        +Date startDate
        +Date endDate
    }}

    class Assignment {{
        +int assignmentId
        +String role
        +String employeeName
    }}

    @enduml
""",
"relations":
"""
{{
    "relations": [
        {{
            "name": "employeeAssignedToProject",
            "classes": [
                "Employee",
                "Project"
            ]
        }},
        {{
            "name": "projectSupervisedByManager",
            "classes": [
                "Project",
                "Manager"
            ]
        }}
    ]
}}
"""
},
{
"view_desc": "The view should show the title and publication date of a research paper along with the name and affiliation of the author.",
"ex_meta_1":
"""
@startuml

    class ResearchPaper {{
        +int id
        +String title
        +Date publicationDate
    }}

    @enduml
""",
"ex_meta_2":
"""
@startuml

    class Author {{
        +int id
        +String name
        +String affiliation
    }}

    class Citation {{
        +int citationId
        +Date citationDate
        +String researchPaperTitle
    }}

    @enduml
""",
"relations":
"""
{{
    "relations": [
        {{
            "name": "paperWrittenByAuthor",
            "classes": [
                "ResearchPaper",
                "Author"
            ]
        }}
    ]
}}
"""
},
{
"view_desc": "The view should display the name and price of a product along with the supplier's name and contact information and the warehouse where the product is stored.",
"ex_meta_1":
"""
@startuml

    class Product {{
        +int id
        +String name
        +double price
    }}

    class Warehouse {{
        +int id
        +String name
        +String location
    }}

    @enduml
""",
"ex_meta_2":
"""
@startuml

    class Supplier {{
        +int id
        +String name
        +String contactInfo
    }}

    class SupplyOrder {{
        +int orderId
        +Date orderDate
        +String productName
    }}

    @enduml
""",
"relations":
"""
{{
    "relations": [
        {{
            "name": "productSuppliedBySupplier",
            "classes": [
                "Product",
                "Supplier"
            ]
        }},
        {{
            "name": "productStoredInWarehouse",
            "classes": [
                "Product",
                "Warehouse"
            ]
        }}
    ]
}}
"""
}
]