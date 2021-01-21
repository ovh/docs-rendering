var doorbell = (function() {
  var options = {};
  return {
    send: function(message, email, success, error) {
      if (!message || message.length === 0) throw 'Invalid message value';
      console.log(options);
      console.log(message);

      if (success) success();
    },
    setOption: function(option, value) {
      options[option] = value;
    }
  };
})();

