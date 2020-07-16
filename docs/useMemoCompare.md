# useMemoCompare

This hook gives us the memoized value of an object, but instead of passing an array of dependencies (like with useMemo) 
we pass a custom compare function that gets both the previous and new value. 

The compare function can then compare nested properties, call object methods, or whatever else you need to do in order 
to determine equality. 

If the compare function returns true then the hook returns the old object reference.

```javascript
import { useState } from 'react';
import useMemoCompare from 'beautiful-react-hooks/useMemoCompare';
import useInterval from 'beautiful-react-hooks/useInterval';

const getBlogContent = (id) => {
console.log('Rendering', id);
return `Blog post id: ${id}`;
}

const BlogPageExample = ({ id }) => {
  const [timer, setTimer] = useState(0);
  const compare = (prev) => Number(prev) !== Number(id);
  const content = useMemoCompare(() => getBlogContent(id), compare);
  
    useInterval(() => {
      setTimer(1 + timer);
    }, 1000); 

  return (
    <DisplayDemo>
      <p>{content}</p>
      <p>{timer}s</p>
    </DisplayDemo>
  );
};

<BlogPageExample id="1" /> 
```

Inspired by [useHook](https://usehooks.com/useMemoCompare/) blog.
