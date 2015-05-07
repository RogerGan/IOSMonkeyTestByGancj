// Usage & Customization example
// Save this UIAutoMonkey.js somewhere in your disk to import it and configure it in each of your Instruments instances
#import "./UIAutoMonkey.js"
#import "./monkeysetting.js"

// Configure the monkey: use the default configuration but a bit tweaked
monkey = new UIAutoMonkey()
monkeysettingconfig = new monkeysetting().config;

monkey.config.numberOfEvents = monkeysettingconfig.numberOfEvents;
monkey.config.screenshotInterval = monkeysettingconfig.screenshotInterval;
// Release the monkey!
// 注意检查lockscreen的事件百分比为0，原生的存在bug，锁屏后无法解锁
monkey.RELEASE_THE_MONKEY();