from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class WebUICfg(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get('webuicfg/config.xml', prefix='config')
