function formatData(value, precision, totalLength) {
    // 1. 调用 toFixed() 确保精度，返回一个字符串
    let formattedValue = value.toFixed(precision);

    // 2. 调用 padStart() 确保总长度，返回一个新字符串
    let paddedValue = formattedValue.padStart(totalLength, ' ');

    // 3. 使用模板字面量返回最终结果
    return paddedValue;
}
