import { displayCart, fetchArticles } from "./articles"

console.log("init.ts loaded.")

let createDummyDataDiv = document.createElement("div")
createDummyDataDiv.innerText = "create/replace dummy data"
document.body.appendChild(createDummyDataDiv)
let createDummyDataDiv2 = document.createElement("div")
createDummyDataDiv2.innerText = "create/replace dummy data 222"
document.body.appendChild(createDummyDataDiv2)

// create or replace dummy data on click:
createDummyDataDiv.addEventListener('click', async () => {
    let res = await fetch('http://localhost:5555/dummy-data')
    console.log(await res.text())
});
// create or replace dummy data on click:
createDummyDataDiv2.addEventListener('click', async () => {
    let res = await fetch('http://localhost:5555/dummy-data2')
    console.log(await res.text())
});


fetchArticles()
displayCart()