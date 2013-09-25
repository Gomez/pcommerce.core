<<<<<<< HEAD:src/pcommerce/core/browser/javascripts/as_customer.js
$('document').ready(function() {
=======
(function($) {
  $('document').ready(function() {
>>>>>>> No longer use the deprecated jq alias in JavaScript:pcommerce/core/browser/javascripts/as_customer.js
    var parents = $('#checkout .component:has(.as_customer)');
    parents.each(function() {
      if($(this).find('.as_customer').is(':checked'))
        $(this).find('.address').hide();
    });
    parents.find('.as_customer').click(function() {
      var checkbox = $(this);
      var parent = $(this);
      while(!parent.find('.address').size())
        parent = parent.parent();
      if(checkbox.is(':checked') )
        parent.find('.address').hide();
      else
        parent.find('.address').show();
    });
<<<<<<< HEAD:src/pcommerce/core/browser/javascripts/as_customer.js
});
=======
  });
})(jQuery);
>>>>>>> No longer use the deprecated jq alias in JavaScript:pcommerce/core/browser/javascripts/as_customer.js
