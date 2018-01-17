const argv = require('yargs').argv

// lookup == lookup a stock price
if (argv.lookup == "current_price" || argv.l == "current_price") {
    
    if (argv.ticker || argv.t) {
        console.log(`looking up ${argv.ticker ? argv.ticker : argv.t}`)
    } else {
        return console.error("please enter a stock ticker to lookup");
    }

} else {
    return console.error("please enter a command line argument");
}