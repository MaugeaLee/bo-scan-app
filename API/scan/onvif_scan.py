from fastapi import APIRouter

from API.CONFIG.bogger import BoggerDevLogger

router = APIRouter()
logger = BoggerDevLogger(__name__).logger

@router.get('/get-mac/{ip}')
async def get_mac(ip: str):
    logger.info(f"Get mac address for {ip}")

    soap_request = """
    <Envelope xmlns="http://www.w3.org/2003/05/soap-envelope">
        <Body>
            <GetNetworkInterfaces xmlns="http://www.onvif.org/ver10/device/wsdl" />
        </Body>
    </Envelope>
    """


    return {"msg": f"{ip}"}


