from app.models import Company
from app.schemas.company import CompanyResponseDetail

def transform_to_company_response_detail(company: Company) -> CompanyResponseDetail:
    return CompanyResponseDetail(
        id=company.id,
        name=company.name,
        description=company.description,
        status="Active" if company.mode else "Inactive",
        created_at=company.created_at
    )