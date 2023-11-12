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
2. Install dependencies for frontend and backend
3. Create .env file and add these variables:
    ```
    CMC_API_KEY=your_coinmarketcap_api_key (https://coinmarketcap.com/api/)
    BTC_API_KEY=your_blockcypher_api_key (https://www.blockcypher.com/)
    ETH_API_KEY=your_etherscan_api_key (https://etherscan.io/apis)
    TON_API_KEY=your_toncenter_api_key (https://testnet.toncenter.com/)
    MONGODB_URL=your_mongodb_url
    ```
4. Run backend with `uvicorn main:app`
5. Run frontend with `npm run dev`

To create an order, call POST `/order` with body (you can also read it on backend_url/docs):
```json
{
  "currency": "any currency",  // usd/eur/etc
  "amountFiat": 9999,  // any amount, integer
  "callback_url": "link that will be called after successful payment",
  "sign": "some sign to verify integrity, eg sha256(f'{currency}:{amountEUR}')"
}
```
After that, you will get a response with order id. Then open `frontend_url?oid=order_id` and you will see the payment page

These are simple steps to run the project locally, but for production, 
you should use docker or something like that. Maybe I will add docker-compose later. 
Moreover, blockchains should be changed from testnets to mainnets


## Additional notes
- Currently, the notification is only sent if the user (or server) triggers GET `/order/{_id}`
- Maybe storing data in decimals is better than floats, but as it is not a fully working project I don't see any reason for changing that at the moment
- After successful payment user can navigate back to currencies etc


