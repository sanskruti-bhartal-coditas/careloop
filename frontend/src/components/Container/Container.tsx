import styles from "./Container.module.scss"
import { Outlet } from "react-router-dom";

const Container = () =>{
  return(
    <section className={styles.container}>
      <Outlet/>
    </section>
  )
}

export default Container;