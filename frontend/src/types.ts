export class Currency {
  name: string;
  color: string;

  constructor(name: string = "", color: string = "") {
    this.name = name;
    this.color = color;
  }
}

export class Order {
  _id: string = "";
  currency: string = "";
  currencyCrypto: string = "";
  amountFiat: number = -1;
  amountCrypto: number = -1;
  description: string = "";
  created_at: string = "";
  email: string = "";
  status: number = -1;
  address: string = "";
  stage: number = -1;
  callback_url: string = "";
  sign: string = "";
}

export type CryptoCurrencyType = {
  BTC: { color: string };
  ETH: { color: string };
  USDT: { color: string };
  TON: { color: string };
};
