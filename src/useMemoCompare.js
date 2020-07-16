import { useEffect, useRef } from 'react';

/**
 * This hook gives us the memoized value of an object, but instead of passing an array of dependencies
 * (like with useMemo) we pass a custom compare function that gets both the previous and new value.
 * The compare function can then compare nested properties, call object methods, or whatever else you need to do in
 * order to determine equality.
 * If the compare function returns true then the hook returns the old object reference.
 * @param fn
 * @param comparingFn
 * @returns {*}
 */
const useMemoCompare = (fn, comparingFn) => {
  const valueRef = useRef();
  const isEqual = comparingFn(valueRef.current);

  // perform the fn on the first render
  useEffect(() => {
    valueRef.current = fn();
  }, []);

  // If not equal update previous to new value (for next render)
  // and then return new new value below.
  useEffect(() => {
    if (!isEqual) {
      valueRef.current = fn(valueRef.current);
    }
  }, [isEqual]);

  return valueRef.current;
};

export default useMemoCompare;
