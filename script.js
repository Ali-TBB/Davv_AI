// Sample product data
const products = [
  {
    name: "Product 1",
    price: 10.99,
    image: "product1.jpg",
    description: "This is a great product!"
  },
  {
    name: "Product 2",
    price: 19.99,
    image: "product2.jpg",
    description: "Another fantastic product!"
  },
  {
    name: "Product 3",
    price: 25.99,
    image: "product3.jpg",
    description: "This product is amazing!"
  }
];

// Get the products container
const productGrid = document.querySelector('.product-grid');

// Create product elements dynamically
products.forEach(product => {
  const productElement = document.createElement('div');
  productElement.classList.add('product');

  // Add image
  const image = document.createElement('img');
  image.src = product.image;
  image.alt = product.name;
  productElement.appendChild(image);

  // Add name and price
  const productName = document.createElement('h3');
  productName.textContent = product.name;
  productElement.appendChild(productName);

  const productPrice = document.createElement('p');
  productPrice.textContent = `$${product.price}`;
  productElement.appendChild(productPrice);

  // Add description
  const productDescription = document.createElement('p');
  productDescription.textContent = product.description;
  productElement.appendChild(productDescription);

  // Add to Cart button (for demo, just logs to console)
  const addToCartButton = document.createElement('button');
  addToCartButton.textContent = 'Add to Cart';
  addToCartButton.addEventListener('click', () => {
    console.log(`Adding ${product.name} to cart`);
  });
  productElement.appendChild(addToCartButton);

  // Add the product element to the grid
  productGrid.appendChild(productElement);
});