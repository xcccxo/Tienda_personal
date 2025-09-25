// ===== Obtener CSRF token =====
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// ===== Wishlist =====
async function addWishlist(productId) {
    try {
        const response = await fetch('/api/wishlist/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ product: productId })
        });
        if (response.ok) {
            alert('Producto agregado a favoritos!');
        } else {
            alert('Error al agregar a favoritos.');
        }
    } catch (error) {
        console.error(error);
        alert('Error al conectar con el servidor.');
    }
}

// ===== Carrito =====
async function addCart(productId) {
    try {
        const response = await fetch('/api/cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ product: productId, quantity: 1 })
        });
        if (response.ok) {
            alert('Producto agregado al carrito!');
        } else {
            alert('Error al agregar al carrito.');
        }
    } catch (error) {
        console.error(error);
        alert('Error al conectar con el servidor.');
    }
}

// ===== Google Maps =====
function initMap() {
    const storeLocation = { lat: 19.4326, lng: -99.1332 }; // CDMX ejemplo
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: storeLocation,
    });
    new google.maps.Marker({
        position: storeLocation,
        map: map,
        title: "MyStore",
    });
}

