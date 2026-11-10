<?php
/**
 * Plugin Name:       نقشه محدوده پشتیبانی پیام‌گستر
 * Plugin URI:        https://www.payamgostar.com/
 * Description:       نقشه‌ی تعاملی محدوده‌ی پشتیبانی حضوری پیام‌گستر در تهران و اطراف (حضوری، با هزینه ایاب و ذهاب، نیازمند تأیید فروشنده). با شورت‌کد [payamgostar_support_map] یا بلوک «نقشه محدوده پشتیبانی» در هر برگه نمایش دهید.
 * Version:           5.0.0
 * Requires at least: 5.8
 * Requires PHP:      7.4
 * Author:            پیام‌گستر
 * License:           GPL-2.0-or-later
 * Text Domain:       payamgostar-support-map
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'PGSM_VERSION', '5.0.0' );
define( 'PGSM_FILE', __FILE__ );
define( 'PGSM_URL', plugin_dir_url( __FILE__ ) );
define( 'PGSM_OPTION', 'pgsm_settings' );

/** Default settings, merged with what the admin saved. */
function pgsm_settings() {
	$defaults = array(
		'height'        => '720px',
		'mobile_height' => '85vh',
		'radius'        => '18',
		'fullscreen'    => 'yes',
	);
	$saved = get_option( PGSM_OPTION, array() );
	return wp_parse_args( is_array( $saved ) ? $saved : array(), $defaults );
}

/** Accept CSS lengths like 720px, 80vh, 100%, 40rem; fall back otherwise. */
function pgsm_clean_length( $value, $fallback ) {
	$value = trim( (string) $value );
	if ( preg_match( '/^\d{1,4}(\.\d+)?(px|vh|svh|dvh|%|rem|em)$/', $value ) ) {
		return $value;
	}
	if ( preg_match( '/^\d{2,4}$/', $value ) ) {
		return $value . 'px';
	}
	return $fallback;
}

/** URL of the map page; the version query string busts caches after updates. */
function pgsm_map_url() {
	return add_query_arg( 'ver', PGSM_VERSION, PGSM_URL . 'assets/map.html' );
}

/**
 * Render the map. The map is a full-screen app, so it runs in an isolated frame:
 * the site theme cannot break its layout and its styles never leak into the site.
 */
function pgsm_render( $atts = array() ) {
	$s    = pgsm_settings();
	$atts = shortcode_atts(
		array(
			'height'        => $s['height'],
			'mobile_height' => $s['mobile_height'],
			'radius'        => $s['radius'],
			'fullscreen'    => $s['fullscreen'],
		),
		$atts,
		'payamgostar_support_map'
	);

	$height  = pgsm_clean_length( $atts['height'], '720px' );
	$mheight = pgsm_clean_length( $atts['mobile_height'], '85vh' );
	$radius  = max( 0, min( 40, (int) $atts['radius'] ) );
	$full    = in_array( strtolower( (string) $atts['fullscreen'] ), array( 'yes', '1', 'true', 'on' ), true );
	$id      = 'pgsm-' . wp_unique_id();
	$url     = pgsm_map_url();

	$css = sprintf(
		'#%1$s{position:relative;width:100%%}#%1$s .pgsm-frame{height:%2$s;border-radius:%3$dpx;overflow:hidden;background:#EDEDE8;box-shadow:0 18px 40px -24px rgba(28,31,35,.45)}'
		. '#%1$s iframe{display:block;width:100%%;height:100%%;border:0}'
		. '#%1$s .pgsm-full{position:absolute;left:12px;top:12px;z-index:2;font:600 12px/1 Tahoma,sans-serif;color:#1C1F23;background:rgba(255,255,255,.88);'
		. 'padding:9px 12px;border-radius:10px;text-decoration:none;box-shadow:0 4px 14px -6px rgba(28,31,35,.4);direction:rtl}'
		. '#%1$s .pgsm-full:hover,#%1$s .pgsm-full:focus{background:#fff;color:#B8460F}'
		. '@media (max-width:720px){#%1$s .pgsm-frame{height:%4$s;border-radius:%5$dpx}#%1$s .pgsm-full{position:static;display:inline-block;margin-top:10px;box-shadow:none;border:1px solid #E3E5E8}}',
		esc_attr( $id ),
		esc_attr( $height ),
		$radius,
		esc_attr( $mheight ),
		min( $radius, 12 )
	);

	$html  = '<style>' . $css . '</style>';
	$html .= '<div id="' . esc_attr( $id ) . '" class="pgsm-map" dir="rtl">';
	$html .= '<div class="pgsm-frame"><iframe src="' . esc_url( $url ) . '" title="' . esc_attr__( 'نقشه محدوده پشتیبانی حضوری پیام‌گستر', 'payamgostar-support-map' ) . '" loading="lazy" allow="fullscreen" allowfullscreen referrerpolicy="no-referrer-when-downgrade"></iframe></div>';
	if ( $full ) {
		$html .= '<a class="pgsm-full" href="' . esc_url( $url ) . '" target="_blank" rel="noopener">' . esc_html__( 'نمایش تمام‌صفحه', 'payamgostar-support-map' ) . '</a>';
	}
	$html .= '</div>';
	return $html;
}
add_shortcode( 'payamgostar_support_map', 'pgsm_render' );

/** Block editor: a server-rendered block, no build step needed. */
function pgsm_register_block() {
	if ( ! function_exists( 'register_block_type' ) ) {
		return;
	}
	wp_register_script(
		'pgsm-block',
		PGSM_URL . 'assets/block.js',
		array( 'wp-blocks', 'wp-element', 'wp-components', 'wp-block-editor', 'wp-i18n' ),
		PGSM_VERSION,
		true
	);
	register_block_type(
		'payamgostar/support-map',
		array(
			'editor_script'   => 'pgsm-block',
			'render_callback' => function ( $attrs ) {
				return pgsm_render( array_filter( (array) $attrs, 'strlen' ) );
			},
			'attributes'      => array(
				'height'        => array( 'type' => 'string', 'default' => '' ),
				'mobile_height' => array( 'type' => 'string', 'default' => '' ),
			),
		)
	);
}
add_action( 'init', 'pgsm_register_block' );

/* ---------- Settings page (Settings → نقشه پشتیبانی) ---------- */

function pgsm_admin_menu() {
	add_options_page(
		__( 'نقشه محدوده پشتیبانی', 'payamgostar-support-map' ),
		__( 'نقشه پشتیبانی', 'payamgostar-support-map' ),
		'manage_options',
		'pgsm-settings',
		'pgsm_settings_page'
	);
}
add_action( 'admin_menu', 'pgsm_admin_menu' );

function pgsm_register_settings() {
	register_setting(
		'pgsm',
		PGSM_OPTION,
		array(
			'type'              => 'array',
			'sanitize_callback' => function ( $in ) {
				$in = is_array( $in ) ? $in : array();
				return array(
					'height'        => pgsm_clean_length( $in['height'] ?? '', '720px' ),
					'mobile_height' => pgsm_clean_length( $in['mobile_height'] ?? '', '85vh' ),
					'radius'        => (string) max( 0, min( 40, (int) ( $in['radius'] ?? 18 ) ) ),
					'fullscreen'    => ! empty( $in['fullscreen'] ) ? 'yes' : 'no',
				);
			},
		)
	);
}
add_action( 'admin_init', 'pgsm_register_settings' );

function pgsm_settings_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$s = pgsm_settings();
	?>
	<div class="wrap" dir="rtl">
		<h1><?php esc_html_e( 'نقشه محدوده پشتیبانی پیام‌گستر', 'payamgostar-support-map' ); ?></h1>
		<p><?php esc_html_e( 'برای نمایش نقشه، این شورت‌کد را در هر برگه یا نوشته قرار دهید، یا در ویرایشگر بلوک «نقشه محدوده پشتیبانی» را اضافه کنید.', 'payamgostar-support-map' ); ?></p>
		<p><code style="font-size:14px;padding:6px 10px">[payamgostar_support_map]</code></p>
		<p class="description"><?php esc_html_e( 'نمونه با ارتفاع دلخواه:', 'payamgostar-support-map' ); ?> <code>[payamgostar_support_map height="80vh" mobile_height="90vh"]</code></p>

		<form method="post" action="options.php">
			<?php settings_fields( 'pgsm' ); ?>
			<table class="form-table" role="presentation">
				<tr>
					<th scope="row"><label for="pgsm-height"><?php esc_html_e( 'ارتفاع در دسکتاپ', 'payamgostar-support-map' ); ?></label></th>
					<td><input id="pgsm-height" name="<?php echo esc_attr( PGSM_OPTION ); ?>[height]" type="text" value="<?php echo esc_attr( $s['height'] ); ?>" class="regular-text" dir="ltr">
					<p class="description"><?php esc_html_e( 'مثلاً 720px یا 80vh', 'payamgostar-support-map' ); ?></p></td>
				</tr>
				<tr>
					<th scope="row"><label for="pgsm-mheight"><?php esc_html_e( 'ارتفاع در موبایل', 'payamgostar-support-map' ); ?></label></th>
					<td><input id="pgsm-mheight" name="<?php echo esc_attr( PGSM_OPTION ); ?>[mobile_height]" type="text" value="<?php echo esc_attr( $s['mobile_height'] ); ?>" class="regular-text" dir="ltr"></td>
				</tr>
				<tr>
					<th scope="row"><label for="pgsm-radius"><?php esc_html_e( 'گردی گوشه‌ها (پیکسل)', 'payamgostar-support-map' ); ?></label></th>
					<td><input id="pgsm-radius" name="<?php echo esc_attr( PGSM_OPTION ); ?>[radius]" type="number" min="0" max="40" value="<?php echo esc_attr( $s['radius'] ); ?>" class="small-text"></td>
				</tr>
				<tr>
					<th scope="row"><?php esc_html_e( 'دکمه تمام‌صفحه', 'payamgostar-support-map' ); ?></th>
					<td><label><input name="<?php echo esc_attr( PGSM_OPTION ); ?>[fullscreen]" type="checkbox" value="1" <?php checked( 'yes', $s['fullscreen'] ); ?>> <?php esc_html_e( 'نمایش دکمه «نمایش تمام‌صفحه» روی نقشه', 'payamgostar-support-map' ); ?></label></td>
				</tr>
			</table>
			<?php submit_button( __( 'ذخیره تنظیمات', 'payamgostar-support-map' ) ); ?>
		</form>

		<h2><?php esc_html_e( 'پیش‌نمایش', 'payamgostar-support-map' ); ?></h2>
		<div style="max-width:1100px"><?php echo pgsm_render(); // phpcs:ignore WordPress.Security.EscapeOutput -- built from escaped parts ?></div>
	</div>
	<?php
}

/** Quick link from the Plugins screen to the settings page. */
add_filter(
	'plugin_action_links_' . plugin_basename( __FILE__ ),
	function ( $links ) {
		array_unshift( $links, '<a href="' . esc_url( admin_url( 'options-general.php?page=pgsm-settings' ) ) . '">' . esc_html__( 'تنظیمات', 'payamgostar-support-map' ) . '</a>' );
		return $links;
	}
);
