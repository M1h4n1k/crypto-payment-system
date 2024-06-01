# Crypto payment system
![](/images/default.png)

## What is it?
It's a simple payment system that can collect 3 multiple cryptocurrencies. 
Currently only btc, eth and ton are supported

## Why?
Mainly because I want to practise a bit in webdev and get a small weekend-pet project. 
And one of the reasons is that I'm not really satisfied with other systems on the market. 
So maybe I will use it later and add other payment systems

## Stack?
**Vue.js** + **TailwindCSS** on frontend and **FastAPI** + **mongoDB** on backend. 
Also, different APIs are used for getting information about blockchain transactions

## How to use?
1. Clone the repo
2. Install docker and docker compose
3. Create .env file in `backend/` and add these variables:
    ```
    CMC_API_KEY=your_coinmarketcap_api_key (https://coinmarketcap.com/api/)
    BTC_API_KEY=your_blockcypher_api_key (https://www.blockcypher.com/)
    ETH_API_KEY=your_etherscan_api_key (https://etherscan.io/apis)
    TON_API_KEY=your_toncenter_api_key (https://testnet.toncenter.com/)
    MONGODB_URL=your_mongodb_url (by default mongo is running on - mongodb://mongo:27017)
    ```
4. Create .env file in `frontend/` and add `VITE_API_URL = "BACKEND URL"` (if running locally with default docker-compose it is http://localhost:3001)
5. Run `docker compose up -d --build` to run all containers. 
6. Navigate to backend_url/docs (backend_url is `http://localhost:3000` by default), select POST /order and create an order with e.g. such payload:
```json
{
  "currency": "ETH",
  "amountFiat": 9999,
  "callback_url": "http://localhost:3000",
  "sign": "123123"
}
```
7. You will get a response with order id. Open `frontend_url?oid=order_id` (frontend_url is `http://localhost:3000` by default) and you will see the payment page

### NB:
Blockchains should be changed from testnets to mainnets if running production


## Additional notes
- Currently, the notification is only sent if the user (or server) triggers GET `/order/{_id}`
- Maybe storing data in decimals is better than floats, but as it is not a fully working project I don't see any reason for changing that at the moment
- After successful payment user can navigate back to currencies etc


