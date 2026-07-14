import styles from "./Loader.module.scss";
import type { LoaderProps } from "./Loader.types";

const Loader = ({ message = "Loading..." }: LoaderProps) => {
  return (
    <div className={styles.loader}>
      <div>
        <h3>{message}</h3>
      </div>
    </div>
  );
};

export default Loader;