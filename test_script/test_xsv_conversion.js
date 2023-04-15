function convertListOfListToXSVString(resultMatrix, delimeter = ",") {
  console.log(`convertListOfListToXSV: row: ${resultMatrix.length}`);

  if (resultMatrix.length > 0) {
    console.log(
      `convertListOfListToXSV: row: ${resultMatrix.length}, column: ${resultMatrix[0].length}`
    );
  }

  let resultString = "";

  resultMatrix.forEach((row) => {
    let rowString = row.join(delimeter);
    resultString += rowString + "\n";
  });

  return resultString;
}

let resultMatrix = [
  ["columnA", "columnB"],
  [0, 1],
  [2, 3],
];

let resultXSVString = convertListOfListToXSVString(
  resultMatrix,
  ","
);

console.log(`resultXSVString: ${resultXSVString}`);
