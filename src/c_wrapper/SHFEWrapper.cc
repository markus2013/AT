#include "SHFEWrapper.h"
#include <iostream>
#include <cstring>

struct DetailReader
{
    DetailReader(const std::string& detail)
    {}

    // Basically strtok is more efficient, but don't care...
    bool next(std::pair<std::string, std::string>& res)
    {
        if (_detial.empty()) return false;

        std::string tag_value;

        size_t pos = _detail.find('|');
        
        if (pos != std::string::npos)
        {
            tag_value = _detail.substr(0, pos);
            _detail.erase(0, pos+1);
        }
        else
        {
            tag_value = _detail;
            _detial.clean();
        }

        pos = tag_value.find('=');
        if (pos == std::string::npos)
            return false;
        res.first  = tag_value.substr(0, pos);
        res.second = tag_value.substr(pos+1);
    }

private:
    const std::string& _detail;
};


template <size_t N>
void assign(char (&dest)[N], const std::string& src)
{
    std::strncpy(dest, src, N);
}

template <typename T>
void assing(T& dest, const T& src)
{
    dest = src;
}

template <typename T>
bool fillOrder(T& order, const std::string& detail, int requestId)
{
	DetailReader r(detail);
	
	assign(order.BrokerID, _broker);
	assign(order.UserID, _user);
	
	assign(order.OrderPriceType, THOST_FTDC_OPT_LimitPrice);
	assign(order.TimeCondition, THOST_FTDC_TC_IOC);
	
	assign(order.IsAutoSuspend, 1);
	assign(order.
	
	std::pair<std::string, std::string> tag_value;
	while(r.next(tag_value))
	{
		if (tag_value.first == "investor")
			assign(order.InvestorID, tag_value.second);
		else
		if (tag_value.first == "instrument")
			assign(order.InstrumentID, tag_value.second);
		else
		if (tag_value.first == "reference")
			assign(order.OrderRef, tag_value.second);
		else
		if (tag_value.first == "price")
			assign(order.LimitPrice, double(atof(tag_value.second));
		else
		if (tag_value.first == "volume")
			assign(order.VolumeTotalOriginal, atoi(tag_value.second));
	};
	
	order.RequestID = requestId;
	
	return order.InstrumentID[0] && order.OrderRef[0] && order.LimitPrice && order.VolumeTotalOriginal;
}

bool SHFEWrapper::start(const std::string& detail)
{
    if (detail.empty())
        return false;

    DetailReader r(detail);

    std::pair<std::string, std::string> tag_value;
    while(r.next(tag_value))
    {
        if (tag_value.first == "front")
            _front = tag_value.second;
        else
        if (tag_value.first == "user")
            _user = tag_value.second;
        else
        if (tag_value.first == "pass")
            _password = tag_value.second;
        else
        if (tag_value.first == "broker")
            _broker = tag_value.second;
        else
        {
            // TODO: use call back to notify the error?
            std::cout << "Unknown tag: " << tag.first << std::endl;
            return false;
        }
    };

    if (front.empty() || user.empty() || pass.empty())
    {
        // TODO: use call back to notify the error
        return false;
    }

    // TODO: start connect front
    _api->RegisterFront(const_cast<char*>(front.c_str()));

    return true;
}

void SHFEWrapper::OnFrontConnected()
{
    _date.assign(shfe.GetTradingDay);
    
    CThostFtdcReqUserLoginField login;
    memset(&login, 0, sizeof(login));
    
    // Need to check what is necessary...
	// Maybe broker id is not necessary either.
    assign(login.TradingDay, _date);
    assign(login.BrokerID, _brokerId);
    assign(login.UserID, _user);
    assign(login.Password, _password);
    assign(login.UserProductInfo, std::string("ATv1000");
    
    _api->ReqUserLogin(&login, getRequestID());
}

bool SHFEWrapper::insertOrder(const std::string& detail)
{
	CThostFtdcInputOrderField order;
	std::memset(&order, 0, sizeof(order));
   
	if (!fillOrder(order, detail, getRequestID()))
		return false;
	
	_api->ReqOrderInsert(&order, order->RequestID);
	return true;
}

// If all orders are IOC.... we don't need this at all
bool SHFEWrapper::changeOrder(const std::string& detail)
{
	CThostFtdcInputOrderActionField order;
	std::memset(&order, 0, sizeof(order));

	assign(order.ActionFlag, THOST_FTDC_AF_Modify);
	if (!fillOrder(order, detail, getRequestID()))
		return false;

	_api->ReqOrderAction(&order, order->RequestID);

	return true;
}

// If all orders are IOC... we don't need this at all
bool SHFEWrapper::deleteOrder(const std::string& detail)
{
	CThostFtdcInputOrderActionField order;
	std::memset(&order, 0, sizeof(order));

	assign(order.ActionFlag, THOST_FTDC_AF_Delete);
	if (!fillOrder(order, detail, getRequestID()))
		return false;
		
	_api->ReqOrderAction(&order, order->RequestID);

	return true;
}

static SHFEWrapper shfe;

bool initialize(const char* detail)
{
    std::cout << "Initialize" << std::endl;
    shfe.start(detail);
}

bool finalize()
{
    std::cout << "Finalize" << std::endl;
}

bool registerCallback(Callback callback)
{
    shfe.registerCallback(callback);
}

bool insertOrder(const char* detail)
{
    return shfe.insertOrder(detail);
}

bool changeOrder(const char* detail)
{
    return shfe.changeOrder(detail);
}

bool deleteOrder(const char* detail)
{
    return shfe.deleteOrder(detail);
}
