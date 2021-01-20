var doorbell = (function() {
  var options = {};
  return {
    send: function(message, email, success, error) {
      console.log(options);
      console.log(message);

      if (success) success();
    },
    setOption: function(option, value) {
      options[option] = value;
    }
  };
})();

