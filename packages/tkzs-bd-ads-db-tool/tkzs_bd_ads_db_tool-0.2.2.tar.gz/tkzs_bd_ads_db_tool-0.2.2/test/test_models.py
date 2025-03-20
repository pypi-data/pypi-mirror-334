from tkzs_bd_db_tool import get_session,init_db
from tkzs_bd_db_tool import models


class TestModels(object):
    def __init__(self):
        init_db()
    
    def test_BdAuthTokenTable(self):
        with get_session() as session:
            rsp = session.query(models.BdAuthTokenTable).all()
            for item in rsp:
                rsp_dict = item.to_dict()
                print(rsp_dict)
    def test_BdAdMaterialTransferTable(self):
        with get_session() as session:
            rsp = session.query(models.BdAdMaterialTransferTable).all()
            for item in rsp:
                rsp_dict = item.to_dict()
                print(rsp_dict)
    def test_BdAdCenterBindTable(self):
        with get_session() as session:
            rsp = session.query(models.BdAdCenterBindTable).all()
            for item in rsp:
                rsp_dict = item.to_dict()
                print(rsp_dict)
    def test_LeadsNoticePush(self):
        with get_session() as session:
            rsp = session.query(models.LeadsNoticePush).all()
            for item in rsp:
                rsp_dict = item.to_dict()
                print(rsp_dict)
    def test_BaiduAccoutCostRrport(self):
        with get_session() as session:
            rsp = session.query(models.BaiduAccoutCostRrport).all()
            for item in rsp:
                rsp_dict = item.to_dict()
                print(rsp_dict)
    def test_account_mapping(self):
        with get_session() as session:
            rsp = session.query(models.BdAdCenterBindTable).all()
            account_mapping = models.BdAdCenterBindTable.to_account_mapping(rsp)
            print(account_mapping)

if __name__ == '__main__':
    test = TestModels()
    # test.test_BdAuthTokenTable()
    # test.test_BdAdMaterialTransferTable()
    # test.test_BdAdCenterBindTable()
    # test.test_LeadsNoticePush()
    # test.test_BaiduAccoutCostRrport()
    test.test_account_mapping()
    
