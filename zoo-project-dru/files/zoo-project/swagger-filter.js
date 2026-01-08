// swagger-filter.js - Complete version
(function() {
    'use strict';
  
    // === EXACT SCRIPT FOR YOUR MODAL ===
    function keepOnlyImplicitFlow() {
        const modal = document.querySelector('.dialog-ux');
        if (!modal) return;
        
        // Find all authentication containers
        const authContainers = modal.querySelectorAll('.auth-container');
        
        authContainers.forEach(container => {
            // Check if this container contains the "implicit" flow
            const h4Element = container.querySelector('h4');
            if (h4Element && h4Element.textContent.includes('(OAuth2, implicit)')) {
                // Keep visible the one we want
                container.style.display = 'block';
                
                // Re-enable the buttons (they are set to display: none)
                const buttons = container.querySelectorAll('.btn');
                buttons.forEach(btn => {
                    btn.style.display = 'block';
                });
            } else {
            // Hide all other containers
            container.style.display = 'none';
            }
        });
        
        // Also hide duplicate introduction texts (keep only the first one)
        const scopeDefs = modal.querySelectorAll('.scope-def');
        for (let i = 1; i < scopeDefs.length; i++) {
            scopeDefs[i].style.display = 'none';
        }

        authContainers.forEach(container => {
            if(container.style.display ==='block'){
                const scopes = container.querySelectorAll('.scope-def');
                scopes.forEach(scope => {
                    scope.style.display = 'block';
                });
            }

            
        });
    }

    // Function to detect and process modal opening
    function setupModalObserver() {
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
        if (mutation.addedNodes.length > 0) {
            const modal = document.querySelector('.dialog-ux');
            if (modal) {
                // Apply filtering as soon as the modal is detected
                keepOnlyImplicitFlow();
                
                // Stop observation once the modal has been processed
                //observer.disconnect();
            }
        }
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
    }

    // Start observation
    setupModalObserver();

    // Listen for clicks on the main Authorize button
    document.addEventListener('click', (e) => {
    if (e.target.classList.contains('authorize')) {
        // The modal opens with a delay, so we check periodically
        const checkModal = setInterval(() => {
        if (document.querySelector('.dialog-ux')) {
            keepOnlyImplicitFlow();
            clearInterval(checkModal);
        }
        }, 100);
    }
    });

    console.log('✅ Filtering configured: only the OAuth2 implicit section will be visible');

})();
