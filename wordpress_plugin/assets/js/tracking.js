jQuery(document).ready(function($) {
    var idleTime = 0;
    var pagesViewed = 0;
    var sessionStart = Date.now();

    // Track page views
    pagesViewed++;

    // Track idle time
    $(document).on('mousemove keydown scroll', function() {
        idleTime = 0;
    });

    // Send behavior data every 30 seconds or when idle for 1 minute
    setInterval(function() {
        idleTime++;

        // Send behavior data every 30 seconds OR when idle for 1 minute
        if (idleTime % 30 === 0 || idleTime >= 60) {
            $.post(scr_ajax.ajax_url, {
                action: 'scr_update_behavior',
                idle_time: idleTime,
                pages_viewed: pagesViewed,
                session_duration: (Date.now() - sessionStart) / 1000
            });

            // If idle for 1+ minute, also check for abandonment
            if (idleTime >= 60) {
                $.post(scr_ajax.ajax_url, {
                    action: 'scr_cart_update'
                });
            }
        }

        // If idle for more than 10 minutes, keep sending updates
        if (idleTime > 600) {  // 10 minutes
            $.post(scr_ajax.ajax_url, {
                action: 'scr_update_behavior',
                idle_time: idleTime,
                pages_viewed: pagesViewed,
                session_duration: (Date.now() - sessionStart) / 1000
            });
        }
    }, 1000);  // Every second

    // On cart update, send data
    $(document).on('added_to_cart', function() {
        console.log('SCR: Item added to cart, sending data');

        // Check if user is logged in
        if (typeof scr_ajax !== 'undefined' && !scr_ajax.is_user_logged_in) {
            // Show email collection popup for guest users
            showEmailCollectionPopup();
        }

        // Get cart data and send to PHP handler
        $.post(scr_ajax.ajax_url, {
            action: 'scr_cart_update'
        }, function(response) {
            console.log('SCR: Cart update response:', response);
        });
    });

    // Also trigger on page load to check existing cart
    if (typeof wc_cart_fragments_params !== 'undefined') {
        $(document.body).trigger('wc_fragment_refresh');
    }

    // Email collection popup function
    function showEmailCollectionPopup() {
        if ($('#scr-email-popup').length === 0) {
            $('body').append(`
                <div id="scr-email-popup" style="
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    background: rgba(0,0,0,0.7); z-index: 999999; display: flex;
                    align-items: center; justify-content: center;">
                    <div style="
                        background: white; padding: 30px; border-radius: 10px;
                        max-width: 400px; width: 90%; text-align: center;">
                        <h3>Don't Lose Your Cart!</h3>
                        <p>Enter your email to save your cart and get recovery offers:</p>
                        <input type="email" id="scr-guest-email" placeholder="your@email.com"
                               style="width: 100%; padding: 10px; margin: 15px 0; border: 1px solid #ddd; border-radius: 5px;">
                        <div>
                            <button id="scr-save-email" style="
                                background: #007cba; color: white; border: none; padding: 10px 20px;
                                border-radius: 5px; cursor: pointer; margin-right: 10px;">Save Cart</button>
                            <button id="scr-skip-email" style="
                                background: #ddd; color: #333; border: none; padding: 10px 20px;
                                border-radius: 5px; cursor: pointer;">Skip</button>
                        </div>
                    </div>
                </div>
            `);

            // Handle save email
            $('#scr-save-email').on('click', function() {
                var email = $('#scr-guest-email').val();
                if (email) {
                    $.post(scr_ajax.ajax_url, {
                        action: 'scr_save_guest_email',
                        email: email
                    }, function(response) {
                        $('#scr-email-popup').remove();
                        console.log('SCR: Guest email saved:', email);
                    });
                }
            });

            // Handle skip
            $('#scr-skip-email').on('click', function() {
                $('#scr-email-popup').remove();
            });
        }
    }
});