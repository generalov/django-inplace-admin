(function ($) {

    var FIELD_CLASS = 'field-value';
    var DEFAULTS =  {
	urlBase: '/inplaceadmin/',
        formId: 'django_inplaceadmin',
        errorClass: 'error',
        cancelBtnName: 'cancel',
        saveBtnName: 'save',
	editableClass: 'editable'
    };

    function findFields(addr) {
	var ms = addr.split('-');
	var parts = [FIELD_CLASS, [ms[0], ms[1], ms[2]].join('-'), ms[3]];

	return $('.' + parts.join('.'));
    }

    $.fn.djangoEditable = function (options) {
        var opts = $.extend({}, $.fn.djangoEditable.defaults, options);
	var addr = opts.addr;
	var urlChange = opts.url || opts.urlBase + opts.addr + '/';

        return this.each(function () {
            var obj = $(this);

            function save () {
		var form = $('#' + opts.formId);

                $.ajax({
                    type: "PUT",
                    url: urlChange, 
                    data: form.serialize(),
                    success: function (html, text_status) {
			var fields = findFields(addr);

			fields
			    .html(html)
			;
			form
			    .remove()
			;
                        obj
			    .show()
			;
                    },
		    error: function (xhr, b, d,f) {
			var html = xhr.responseText;

			gotForm(html, b);
		    }
                });  

		return false;
            }

            function cancel () {
		var form = $('#' + opts.formId);

                obj
		    .show()
		;
		form
		    .remove()
		;

		return false;
            }

            function gotForm (html, text_status) {
		if (!html) {
		    /// console.log('connection error');
		    return;
		}

		var prevform = $('#' + opts.formId);

		if (prevform.length) {
		    var prevobj = prevform.get(0).obj;

		    prevobj
			.show()
		    ;
		    prevform
			.remove()
		    ;
		}

                var form = $(html); 
		form.get(0).obj = obj;

                obj
                    .hide()
                    .after(form)
                ;

		var editor = $(':input:visible:enabled:first', form);
		var saveBtn =$('[name=' + opts.saveBtnName + ']', form);
		var cancelBtn = $('[name=' + opts.cancelBtnName + ']', form);

                editor
                    .focus()
                    .keyup(function (event) {
                        var keycode = event.which;
                      
                        if (keycode == 27) {
                            return cancel();
                        }
                    })
                ;

                saveBtn
		    .click(save)
		;

                cancelBtn
		    .click(cancel)
		;
            }
            
            $(this).click(function () {
                $.get(urlChange, {}, gotForm, 'html');
            });
        });
    }

    $.fn.djangoEditable.defaults = DEFAULTS;

    var fieldAddrRe = new RegExp(FIELD_CLASS + " ([^ ]+)-([^ ]+)-(\\d+) ([^ ]+)");

    function addrFromString (str) {
	if (!str) return false;
	var ms = str.match(fieldAddrRe); 
	var addr = ms ? ms.slice(1).join('-'): false;

	return addr;
    }

    $.fn.djangoClamEditable = function (options) {
        var opts = $.extend({}, $.fn.djangoEditable.defaults, options);
	var r = {};

	this.map(function (){
	    var addr = addrFromString($(this).attr('class'));

	    /// console.log(addr);
	    if (addr) {
		r[addr]='';
	    }
	});

	$.ajax({
	    url: opts.urlBase + 'clam/',
	    type: 'POST',
	    dataType: 'json',
	    data: (r),
	    success: function (data) {
		/// console.log(data);
		var addr;
		var permited = data['permited'];

		for (addr in permited) {
		    var fields = findFields(addr);
		    var urlChange = permited[addr]

		    fields
			.addClass(opts.editableClass)
			.djangoEditable({
			    addr: addr,
			    url: urlChange
			});
		}
	    }
	});

	return this;
    };
})(jQuery);
