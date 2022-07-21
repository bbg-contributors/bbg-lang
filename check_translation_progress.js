const { readFileSync } = require("fs");
const argvArray = process.argv.slice(2);

const lang_meta = JSON.parse(readFileSync(__dirname + "/meta.json"));

is_valid_query = false;

console.log("\n现在检查 id 为 " + argvArray[0] + " 的语言的翻译进度。\n");

for (let i = 0; i < lang_meta["名称与文件名之间的映射关系"].length; i++) {
  if (argvArray[0] === lang_meta["名称与文件名之间的映射关系"][i]["id"]) {
    is_valid_query = true;

    console.log("语言名称：" + lang_meta["名称与文件名之间的映射关系"][i]["name"]);
    console.log("语言id：" + lang_meta["名称与文件名之间的映射关系"][i]["id"] + "\n");

    const lang_current = JSON.parse(readFileSync(__dirname + `/multi_language/${argvArray[0]}.json`));

    const keysTotalNumber = lang_meta["需要翻译的键值"].length;

    keysCurrentNumber = 0;

    for (let j = 0; j < keysTotalNumber; j++) {
      if (lang_current[lang_meta["需要翻译的键值"][j]] !== undefined && lang_current[lang_meta["需要翻译的键值"][j]] !== null) {
        keysCurrentNumber++;
      }
    }

    console.log("有效的已翻译键值数：" + keysCurrentNumber);
    console.log("总共需要翻译的键值数：" + keysTotalNumber + "\n");

    console.log("翻译进度百分比：" + (keysCurrentNumber / keysTotalNumber) * 100 + "%" + "\n");
  }
}

if (is_valid_query !== true) {
  console.log("元文件中没有记录 id 为 " + argvArray[0] + " 的语言，所以检查失败。如果这是你打算翻译的新语言，请先在元文件（meta.json）中加入有关该语言的信息。\n");
}
