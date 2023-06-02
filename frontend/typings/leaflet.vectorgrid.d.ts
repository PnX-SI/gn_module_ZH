// in the global namesapce "L"
declare namespace L {
  // there is a child namespace "vectorGrid"
  namespace vectorGrid {
    // which has a function call "slicer" that takes data and optional
    // configurations. To make it simple, we don't specify the input
    // and output types.
    export function slicer(data: any, options?: any): any;
  }
}
