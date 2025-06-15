// // This function fetches articles and displays them
// export async function fetchArticles(): Promise<void> {
//     try {
//         const response = await fetch("http://localhost:5555/api/articles");
//         if (!response.ok) {
//             throw new Error("Failed to fetch articles");
//         }

//         const articles = await response.json();
//         renderArticles(articles);
//     } catch (err) {
//         console.error("Error fetching articles:", err);
//     }
// }

// // Render articles in the grid and add 'Add to Cart' functionality
// function renderArticles(articles: any[]): void {
//     const grid = document.getElementById("article-grid");
//     if (!grid) return;

//     grid.innerHTML = ""; // Clear previous items

//     for (const article of articles) {
//         const card = document.createElement("div");
//         card.className = "card";

//         card.innerHTML = `
//       <h2>${article.artikel_name}</h2>
//       <p><strong>Category:</strong> ${article.category_name}</p>
//       <p class="price">€ ${(article.price_in_cents / 100).toFixed(2)}</p>
//       <p class="stock">In stock: ${article.available_stock}</p>
//     `;

//         const button = document.createElement("button");
//         button.textContent = "Add to Cart";
//         button.onclick = () => {
//             addToCart(article);
//         };

//         card.appendChild(button);
//         grid.appendChild(card);
//     }
// }

// // Function to add an item to the cart and store it in localStorage
// function addToCart(article: any): void {
//     let cart = JSON.parse(localStorage.getItem("cart") || "[]");

//     // Check if item already exists in the cart
//     const existingItem = cart.find((item: any) => item.artikel_id === article.artikel_id);

//     if (existingItem) {
//         // If item exists, increase quantity
//         existingItem.quantity += 1;
//     } else {
//         // If item doesn't exist, add it to the cart with quantity 1
//         cart.push({
//             artikel_id: article.artikel_id,
//             artikel_name: article.artikel_name,
//             price_in_cents: article.price_in_cents,
//             quantity: 1
//         });
//     }

//     // Save the updated cart to localStorage
//     localStorage.setItem("cart", JSON.stringify(cart));
//     alert(`Article "${article.artikel_name}" added to cart!`);
// }

// // Function to display the cart (called when user goes to checkout page)
// export function displayCart(): void {
//     const cart = JSON.parse(localStorage.getItem("cart") || "[]");
//     const cartContainer = document.getElementById("cart-container");

//     if (!cartContainer) return;

//     // Clear the existing cart content
//     cartContainer.innerHTML = "";

//     if (cart.length === 0) {
//         cartContainer.innerHTML = "<p>Your cart is empty!</p>";
//         return;
//     }

//     let totalAmount = 0;

//     // Loop through the cart and render each item
//     cart.forEach((item: any) => {
//         totalAmount += item.price_in_cents * item.quantity;

//         const cartItem = document.createElement("div");
//         cartItem.className = "cart-item";

//         cartItem.innerHTML = `
//             <p>${item.artikel_name} - € ${(item.price_in_cents / 100).toFixed(2)} x ${item.quantity}</p>
//         `;

//         cartContainer.appendChild(cartItem);
//     });

//     const totalPrice = document.createElement("p");
//     totalPrice.className = "total-price";
//     totalPrice.innerHTML = `Total: € ${(totalAmount / 100).toFixed(2)}`;

//     cartContainer.appendChild(totalPrice);
// }

// // Function to handle checkout
// export async function checkout(): Promise<void> {
//     const cart = JSON.parse(localStorage.getItem("cart") || "[]");

//     if (cart.length === 0) {
//         alert("Your cart is empty!");
//         return;
//     }

//     try {
//         const response = await fetch("http://localhost:5555/api/checkout", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//             body: JSON.stringify(cart),
//         });

//         if (!response.ok) {
//             throw new Error("Failed to place the order");
//         }

//         // Clear the cart after successful checkout
//         localStorage.removeItem("cart");

//         alert("Order placed successfully!");
//     } catch (err) {
//         console.error("Error during checkout:", err);
//         alert("Something went wrong during checkout.");
//     }
// }

// // Call the fetch on page load
// fetchArticles();

// // You can call displayCart when rendering the cart page
// // displayCart();
