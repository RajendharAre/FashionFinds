function togglePassword() {
    var passwordInput = document.getElementById("password");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}

// Add to Cart function
function addToCart(productId) {
    // Create a form dynamically and submit it
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/add_to_cart/${productId}`;
    
    // Add CSRF token if needed
    const csrfToken = document.querySelector('meta[name="csrf-token"]');
    if (csrfToken) {
        const tokenInput = document.createElement('input');
        tokenInput.type = 'hidden';
        tokenInput.name = 'csrf_token';
        tokenInput.value = csrfToken.content;
        form.appendChild(tokenInput);
    }
    
    document.body.appendChild(form);
    form.submit();
}

// Add to Wishlist function
function addToWishlist(productId) {
    // Create a form dynamically and submit it
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/add_to_wishlist/${productId}`;
    
    // Add CSRF token if needed
    const csrfToken = document.querySelector('meta[name="csrf-token"]');
    if (csrfToken) {
        const tokenInput = document.createElement('input');
        tokenInput.type = 'hidden';
        tokenInput.name = 'csrf_token';
        tokenInput.value = csrfToken.content;
        form.appendChild(tokenInput);
    }
    
    document.body.appendChild(form);
    form.submit();
}

// Update cart quantity
function updateCartQuantity(productId, quantity) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/update_cart/${productId}`;
    
    const quantityInput = document.createElement('input');
    quantityInput.type = 'hidden';
    quantityInput.name = 'quantity';
    quantityInput.value = quantity;
    form.appendChild(quantityInput);
    
    // Add CSRF token if needed
    const csrfToken = document.querySelector('meta[name="csrf-token"]');
    if (csrfToken) {
        const tokenInput = document.createElement('input');
        tokenInput.type = 'hidden';
        tokenInput.name = 'csrf_token';
        tokenInput.value = csrfToken.content;
        form.appendChild(tokenInput);
    }
    
    document.body.appendChild(form);
    form.submit();
}

// Remove from cart
function removeFromCart(productId) {
    if (confirm('Are you sure you want to remove this item from your cart?')) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/remove_from_cart/${productId}`;
        
        // Add CSRF token if needed
        const csrfToken = document.querySelector('meta[name="csrf-token"]');
        if (csrfToken) {
            const tokenInput = document.createElement('input');
            tokenInput.type = 'hidden';
            tokenInput.name = 'csrf_token';
            tokenInput.value = csrfToken.content;
            form.appendChild(tokenInput);
        }
        
        document.body.appendChild(form);
        form.submit();
    }
}

// Remove from wishlist
function removeFromWishlist(productId) {
    if (confirm('Are you sure you want to remove this item from your wishlist?')) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/remove_from_wishlist/${productId}`;
        
        // Add CSRF token if needed
        const csrfToken = document.querySelector('meta[name="csrf-token"]');
        if (csrfToken) {
            const tokenInput = document.createElement('input');
            tokenInput.type = 'hidden';
            tokenInput.name = 'csrf_token';
            tokenInput.value = csrfToken.content;
            form.appendChild(tokenInput);
        }
        
        document.body.appendChild(form);
        form.submit();
    }
}

// Move from wishlist to cart
function moveToCart(productId) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/move_to_cart/${productId}`;
    
    // Add CSRF token if needed
    const csrfToken = document.querySelector('meta[name="csrf-token"]');
    if (csrfToken) {
        const tokenInput = document.createElement('input');
        tokenInput.type = 'hidden';
        tokenInput.name = 'csrf_token';
        tokenInput.value = csrfToken.content;
        form.appendChild(tokenInput);
    }
    
    document.body.appendChild(form);
    form.submit();
}

// Prevent horizontal scrolling on page load
document.addEventListener('DOMContentLoaded', function() {
    // Ensure body doesn't overflow horizontally
    document.body.style.overflowX = 'hidden';
    document.documentElement.style.overflowX = 'hidden';
    
    // Apply to all forms to prevent accidental horizontal overflow
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.style.maxWidth = '100%';
        form.style.overflowX = 'hidden';
    });
    
    // Apply to all containers
    const containers = document.querySelectorAll('.container, .main-content, .product-container, .brand-container');
    containers.forEach(container => {
        container.style.maxWidth = '100vw';
        container.style.overflowX = 'hidden';
        container.style.boxSizing = 'border-box';
    });
});