import httpx

from fastapi import FastAPI

from ..exception.internal_exception import GatewayTimeoutException, BadGatewayException


async def async_request(app: FastAPI, method, url, current_user: dict = None, **kwargs):
    timeout = httpx.Timeout(connect=app.state.config.REQUEST_CONN_TIMEOUT, read=app.state.config.REQUEST_READ_TIMEOUT,
                            write=app.state.config.REQUEST_WRITE_TIMEOUT, pool=app.state.config.REQUEST_POOL_TIMEOUT)

    if current_user and "access_token" in current_user:
        if "headers" in kwargs.keys():
            kwargs.get("headers")["Authorization"] = f"Bearer {current_user.get('access_token')}"
        else:
            kwargs["headers"] = {
                "Authorization": f"Bearer {current_user.get('access_token')}"
            }

    try:
        async with httpx.AsyncClient(timeout=timeout, verify=False) as client:
            app.state.logger.info(f"async_request() request, url: {url}, method: {method}, kwargs: {kwargs}")
            response = await client.request(method, url, **kwargs)
            app.state.logger.info(
                f"async_request() response, url: {url}, method: {method}, kwargs: {kwargs}, response: {response.text}")
            return response
    except httpx.TimeoutException as exc:
        app.state.logger.warn(
            f"async_request(), TimeoutException, exc: {exc}, url: {url}, method: {method}, kwargs: {kwargs}")
        raise GatewayTimeoutException(str(exc))
    except Exception as exc:
        app.state.logger.warn(
            f"async_request(), Exception, exc: {exc}, url: {url}, method: {method}, kwargs: {kwargs}")
        raise BadGatewayException(str(exc))

async def send_webhook_message(app: FastAPI, message: str):
    if app.state.config.WEBHOOK_BASE_URL:
        payload = {"text": f"【{app.title}】{message}"}
        try:
            await async_request(app, "POST", app.state.config.WEBHOOK_BASE_URL, json=payload)
        except Exception as e:
            app.state.logger.warn(f"Notify failure, Exception:{e}")