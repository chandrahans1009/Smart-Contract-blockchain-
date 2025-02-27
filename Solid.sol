// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Solid {
    uint256 public favoriteNumber;  
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    
    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

 
    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function addPerson(uint256 _favoriteNumber, string memory _name) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }

   
    function getPeopleCount() public view returns (uint256) {
        return people.length;
    }

    // Get details of a specific person by index
    function getPerson(uint256 index) public view returns (uint256, string memory) {
        require(index < people.length, "Index out of bounds");
        People memory person = people[index];
        return (person.favoriteNumber, person.name);
    }
}