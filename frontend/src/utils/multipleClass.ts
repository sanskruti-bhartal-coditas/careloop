export const multipleClass = (classes: Array<string | undefined | null | false>) => {
  return classes.filter(Boolean).join(" ");
};