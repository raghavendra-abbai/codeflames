// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SupplyChain {

struct Product{
uint id;
string name;
string farmer;
uint price;
}

mapping(uint => Product) public products;

function addProduct(
uint id,
string memory name,
string memory farmer,
uint price
) public {

products[id] = Product(id,name,farmer,price);

}

}