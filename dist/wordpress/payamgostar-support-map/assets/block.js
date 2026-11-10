( function ( wp ) {
	var el = wp.element.createElement;
	var __ = wp.i18n.__;
	var be = wp.blockEditor || wp.editor;
	var C = wp.components;
	wp.blocks.registerBlockType( 'payamgostar/support-map', {
		apiVersion: 2,
		title: 'نقشه محدوده پشتیبانی',
		description: 'نقشه‌ی تعاملی محدوده‌ی پشتیبانی حضوری پیام‌گستر',
		icon: 'location-alt',
		category: 'embed',
		keywords: [ 'map', 'نقشه', 'پشتیبانی', 'payamgostar' ],
		supports: { html: false, align: [ 'wide', 'full' ] },
		attributes: {
			height: { type: 'string', default: '' },
			mobile_height: { type: 'string', default: '' }
		},
		edit: function ( props ) {
			var a = props.attributes;
			var blockProps = be.useBlockProps ? be.useBlockProps() : {};
			return el( 'div', blockProps,
				el( be.InspectorControls, null,
					el( C.PanelBody, { title: 'اندازه' },
						el( C.TextControl, { label: 'ارتفاع در دسکتاپ (مثلاً 720px یا 80vh)', value: a.height, onChange: function ( v ) { props.setAttributes( { height: v } ); } } ),
						el( C.TextControl, { label: 'ارتفاع در موبایل (مثلاً 85vh)', value: a.mobile_height, onChange: function ( v ) { props.setAttributes( { mobile_height: v } ); } } )
					)
				),
				el( 'div', { style: { direction: 'rtl', padding: '28px 24px', borderRadius: '16px', background: '#1C1F23', color: '#fff', fontFamily: 'Tahoma, sans-serif' } },
					el( 'div', { style: { width: '40px', height: '4px', borderRadius: '4px', background: '#F26122', marginBottom: '12px' } } ),
					el( 'strong', { style: { fontSize: '16px' } }, 'نقشه محدوده پشتیبانی پیام‌گستر' ),
					el( 'p', { style: { margin: '8px 0 0', color: '#A9ADB4', fontSize: '13px' } }, 'نقشه در صفحه‌ی منتشرشده نمایش داده می‌شود. ارتفاع را از تنظیمات بلوک در ستون کناری تغییر دهید.' )
				)
			);
		},
		save: function () { return null; }
	} );
} )( window.wp );
