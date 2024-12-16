const apiUrl = 'http://localhost:8080/api/producto';

// Función para cargar productos
async function loadProducts() {
  try {
    const response = await fetch(apiUrl);
    const products = await response.json();
    const table = document.getElementById('product-table');
    table.innerHTML = products.map(product => `
      <tr>
        <td>${product.nombre}</td>
        <td>${product.descripcion}</td>
        <td>${product.precio}</td>
        <td>${product.categoria}</td>
        <td>${product.stock}</td>
        <td class="text-center">
          <button onclick="editProduct(${product.id})">✏️</button>
          <button onclick="deleteProduct(${product.id})">❌</button>
        </td>
      </tr>
    `).join('');
  } catch (error) {
    console.error('Error al cargar productos:', error);
  }
}

// Función para agregar un producto
async function addProduct(event) {
  event.preventDefault();
  const form = event.target;
  const product = {
    nombre: form.nombre.value,
    descripcion: form.descripcion.value,
    precio: parseFloat(form.precio.value),
    categoria: form.categoria.value,
    stock: parseInt(form.stock.value),
  };
  try {
    await fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(product),
    });
    loadProducts();
  } catch (error) {
    console.error('Error al agregar producto:', error);
  }
}

// Listeners
document.getElementById('product-form').addEventListener('submit', addProduct);

// Cargar productos al inicio
loadProducts();
