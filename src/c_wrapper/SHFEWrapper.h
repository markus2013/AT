#define ISLIB
#include "ThostFtdcTraderApi.h"

#include <map>
#include <string>

// The message we passed in/out from this module is fix like message
// Don't care about the performance, latency at the moment, otherwise
// this won't be done like this!

typedef void (*Callback)(const char*);

class SHFEWrapper : public CThostFtdcTraderSpi
{
public:
    SHFEWrapper()
        : _requestID()
    {
        _api = CThostFtdcTraderApi::CreateFtdcTraderApi(); 
        _api->Init();
        _api->RegisterSpi(this);
    }

    ~SHFEWrapper()
    {
        _api->Join();
        _api->Release();
    }

    CThostFtdcTraderApi& operator()()
    {	
        return *_api;
    }

    void registerCallback(Callback callback)
    {
        // This might need to be protected from multithreading access
        _callback = callback;
    }

    int getRequestID()
    {
        return _requestID++;
    }

    bool connect(const std::string& detail);
    bool login(const std::string& detail);
    bool insertOrder(const std::string& detail);
    bool changeOrder(const std::string& detail);
    bool deleteOrder(const std::string& detail);

    // API call back we would support
    void OnFrontConnected();
    void OnFrontDisconnected(int nReason){};
    void OnHeartBeatWarning(int nTimeLapse){};
    void OnRspUserLogin(CThostFtdcRspUserLoginField *pRspUserLogin, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {};
    void OnRspUserLogout(CThostFtdcUserLogoutField *pUserLogout, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {};
    void OnRspOrderInsert(CThostFtdcInputOrderField *pInputOrder, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {};
    void OnRspOrderAction(CThostFtdcInputOrderActionField *pInputOrderAction, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {};
    // TODO: Support this later?
    //void OnRspParkedOrderInsert(CThostFtdcParkedOrderField *pParkedOrder, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {};
    void OnRspQryOrder(CThostFtdcOrderField *pOrder, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {};
    void OnRspQryInvestorPosition(CThostFtdcInvestorPositionField *pInvestorPosition, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {};
    void OnRspError(CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {};
    void OnRtnOrder(CThostFtdcOrderField *pOrder) {};
    void OnRtnTrade(CThostFtdcTradeField *pTrade) {};
    void OnErrRtnOrderInsert(CThostFtdcInputOrderField *pInputOrder, CThostFtdcRspInfoField *pRspInfo) {};
    void OnErrRtnOrderAction(CThostFtdcOrderActionField *pOrderAction, CThostFtdcRspInfoField *pRspInfo) {};
    void OnRtnTradingNotice(CThostFtdcTradingNoticeInfoField *pTradingNoticeInfo) {};

private:

    SHFEWrapper(const SHFEWrapper&) {}
    SHFEWrapper& operator == (const SHFEWrapper&) {}

    CThostFtdcTraderApi* _api;
    Callback _callback;

    std::string _front;
    std::string _user;
    std::string _password;
	std::string _broker;
	std::string _date;

    int _requestID;
};

extern "C"
{
bool __declspec(dllexport) initialize(const char*);
bool __declspec(dllexport) finalize();
bool __declspec(dllexport) registerCallback(Callback callback);
bool __declspec(dllexport) insertOrder(const char*);
bool __declspec(dllexport) changeOrder(const char*);
bool __declspec(dllexport) deleteOrder(const char*);
}
