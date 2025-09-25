<?php
// Abandoned Cart Recovery Analytics Dashboard
function scr_display_analytics() {
    global $wpdb;
    $table = $wpdb->prefix . 'cart_logs';

    // Check if table exists, create it if not
    if ($wpdb->get_var("SHOW TABLES LIKE '$table'") != $table) {
        scr_create_tables();
        echo '<div class="notice notice-success"><p>Analytics table created successfully!</p></div>';
    }
    if (isset($_POST['action']) && isset($_POST['cart_ids'])) {
        $action = sanitize_text_field($_POST['action']);
        $cart_ids = array_map('intval', $_POST['cart_ids']);

        if ($action === 'delete' && !empty($cart_ids)) {
            $ids_string = implode(',', $cart_ids);
            $wpdb->query($wpdb->prepare("DELETE FROM $table WHERE id IN ($ids_string)"));
            echo '<div class="notice notice-success"><p>Selected carts deleted successfully.</p></div>';
        } elseif ($action === 'mark_converted' && !empty($cart_ids)) {
            $wpdb->query($wpdb->prepare("UPDATE $table SET converted = 1 WHERE id IN (" . implode(',', $cart_ids) . ")"));
            echo '<div class="notice notice-success"><p>Selected carts marked as converted.</p></div>';
        }
    }

    // Get analytics data
    $total_abandoned = $wpdb->get_var("SELECT COUNT(*) FROM $table WHERE abandoned = 1");
    $total_emails_sent = $wpdb->get_var("SELECT COUNT(*) FROM $table WHERE email_sent = 1");
    $total_opened = $wpdb->get_var("SELECT COUNT(*) FROM $table WHERE opened = 1");
    $total_clicked = $wpdb->get_var("SELECT COUNT(*) FROM $table WHERE clicked = 1");
    $total_converted = $wpdb->get_var("SELECT COUNT(*) FROM $table WHERE converted = 1");

    $open_rate = $total_emails_sent > 0 ? round(($total_opened / $total_emails_sent) * 100, 2) : 0;
    $click_rate = $total_emails_sent > 0 ? round(($total_clicked / $total_emails_sent) * 100, 2) : 0;
    $conversion_rate = $total_emails_sent > 0 ? round(($total_converted / $total_emails_sent) * 100, 2) : 0;

    // Get recent abandoned carts
    $results = $wpdb->get_results("SELECT * FROM $table WHERE abandoned = 1 ORDER BY timestamp DESC LIMIT 50");

    ?>
    <div class="wrap">
        <h1>🛒 Abandoned Cart Recovery Analytics</h1>

        <!-- Analytics Cards -->
        <div class="scr-analytics-cards">
            <div class="scr-card">
                <h3><?php echo $total_abandoned; ?></h3>
                <p>Total Abandoned Carts</p>
            </div>
            <div class="scr-card">
                <h3><?php echo $total_emails_sent; ?></h3>
                <p>Recovery Emails Sent</p>
            </div>
            <div class="scr-card">
                <h3><?php echo $total_opened; ?> (<?php echo $open_rate; ?>%)</h3>
                <p>Emails Opened</p>
            </div>
            <div class="scr-card">
                <h3><?php echo $total_clicked; ?> (<?php echo $click_rate; ?>%)</h3>
                <p>Links Clicked</p>
            </div>
            <div class="scr-card">
                <h3><?php echo $total_converted; ?> (<?php echo $conversion_rate; ?>%)</h3>
                <p>Carts Recovered</p>
            </div>
        </div>

        <!-- Bulk Actions Form -->
        <form method="post" id="scr-analytics-form">
            <div class="tablenav top">
                <div class="alignleft actions bulkactions">
                    <label for="bulk-action-selector-top" class="screen-reader-text">Select bulk action</label>
                    <select name="action" id="bulk-action-selector-top">
                        <option value="-1">Bulk Actions</option>
                        <option value="delete">Delete</option>
                        <option value="mark_converted">Mark as Converted</option>
                    </select>
                    <input type="submit" id="doaction" class="button action" value="Apply">
                </div>
                <br class="clear">
            </div>

            <!-- Abandoned Carts Table -->
            <table class="wp-list-table widefat fixed striped">
                <thead>
                    <tr>
                        <th scope="col" class="manage-column column-cb check-column">
                            <input type="checkbox" id="cb-select-all">
                        </th>
                        <th scope="col">User ID</th>
                        <th scope="col">Email</th>
                        <th scope="col">Cart Items</th>
                        <th scope="col">Abandoned Date</th>
                        <th scope="col">Email Sent</th>
                        <th scope="col">Opened</th>
                        <th scope="col">Clicked</th>
                        <th scope="col">Converted</th>
                        <th scope="col">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <?php if (empty($results)): ?>
                        <tr>
                            <td colspan="10">No abandoned carts found.</td>
                        </tr>
                    <?php else: ?>
                        <?php foreach ($results as $row): ?>
                            <tr>
                                <th scope="row" class="check-column">
                                    <input type="checkbox" name="cart_ids[]" value="<?php echo $row->id; ?>">
                                </th>
                                <td><?php echo esc_html($row->user_id); ?></td>
                                <td><?php echo esc_html($row->email); ?></td>
                                <td>
                                    <?php
                                    $items = json_decode($row->items, true);
                                    if (is_array($items)) {
                                        echo '<ul style="margin: 0; padding-left: 20px;">';
                                        foreach ($items as $item) {
                                            echo '<li>' . esc_html($item['name']) . ' (x' . $item['quantity'] . ')</li>';
                                        }
                                        echo '</ul>';
                                    } else {
                                        echo esc_html($row->items);
                                    }
                                    ?>
                                </td>
                                <td><?php echo date('M j, Y g:i A', strtotime($row->timestamp)); ?></td>
                                <td>
                                    <span class="scr-status <?php echo $row->email_sent ? 'sent' : 'not-sent'; ?>">
                                        <?php echo $row->email_sent ? '✅ Sent' : '❌ Not Sent'; ?>
                                    </span>
                                </td>
                                <td>
                                    <span class="scr-status <?php echo $row->opened ? 'opened' : 'not-opened'; ?>">
                                        <?php echo $row->opened ? '👁️ Opened' : '📧 Not Opened'; ?>
                                    </span>
                                </td>
                                <td>
                                    <span class="scr-status <?php echo $row->clicked ? 'clicked' : 'not-clicked'; ?>">
                                        <?php echo $row->clicked ? '🔗 Clicked' : '🚫 Not Clicked'; ?>
                                    </span>
                                </td>
                                <td>
                                    <span class="scr-status <?php echo $row->converted ? 'converted' : 'not-converted'; ?>">
                                        <?php echo $row->converted ? '💰 Converted' : '🛒 Not Converted'; ?>
                                    </span>
                                </td>
                                <td>
                                    <button type="button" class="button scr-delete-cart" data-id="<?php echo $row->id; ?>">Delete</button>
                                    <?php if (!$row->converted): ?>
                                        <button type="button" class="button scr-mark-converted" data-id="<?php echo $row->id; ?>">Mark Converted</button>
                                    <?php endif; ?>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    <?php endif; ?>
                </tbody>
            </table>
        </form>
    </div>

    <style>
        .scr-analytics-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .scr-card {
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .scr-card h3 {
            margin: 0 0 10px 0;
            font-size: 2em;
            color: #007cba;
        }

        .scr-card p {
            margin: 0;
            color: #666;
            font-weight: 500;
        }

        .scr-status.sent { color: #28a745; }
        .scr-status.not-sent { color: #dc3545; }
        .scr-status.opened { color: #17a2b8; }
        .scr-status.not-opened { color: #6c757d; }
        .scr-status.clicked { color: #ffc107; }
        .scr-status.not-clicked { color: #6c757d; }
        .scr-status.converted { color: #28a745; font-weight: bold; }
        .scr-status.not-converted { color: #6c757d; }

        .tablenav .actions {
            margin-bottom: 15px;
        }

        .scr-delete-cart {
            background: #dc3545;
            color: white;
            border: none;
            padding: 4px 8px;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 5px;
        }

        .scr-mark-converted {
            background: #28a745;
            color: white;
            border: none;
            padding: 4px 8px;
            border-radius: 4px;
            cursor: pointer;
        }

        .scr-delete-cart:hover { background: #c82333; }
        .scr-mark-converted:hover { background: #218838; }
    </style>

    <script>
    jQuery(document).ready(function($) {
        // Select all checkbox
        $('#cb-select-all').on('change', function() {
            $('input[name="cart_ids[]"]').prop('checked', $(this).prop('checked'));
        });

        // Individual delete buttons
        $('.scr-delete-cart').on('click', function() {
            if (confirm('Are you sure you want to delete this cart?')) {
                var cartId = $(this).data('id');
                $('<form method="post"><input type="hidden" name="action" value="delete"><input type="hidden" name="cart_ids[]" value="' + cartId + '"></form>')
                    .appendTo('body').submit();
            }
        });

        // Mark as converted buttons
        $('.scr-mark-converted').on('click', function() {
            var cartId = $(this).data('id');
            $('<form method="post"><input type="hidden" name="action" value="mark_converted"><input type="hidden" name="cart_ids[]" value="' + cartId + '"></form>')
                .appendTo('body').submit();
        });
    });
    </script>
    <?php
}
?>