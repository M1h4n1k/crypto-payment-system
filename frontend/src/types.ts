export class Currency {
  name: string;
  color: string;

  constructor(name: string = "", color: string = "") {
    this.name = name;
    this.color = color;
  }
}

export interface Order {
  _id: string;
  currency: string;
  currencyCrypto: string;
  amountEUR: number;
  amountCrypto: number;
  description: string;
  created_at: string;
  email: string;
  status: number;
  address: string;
  stage: number;
  callback_url: string;
  sign: string;
}
