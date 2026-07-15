import { NavLink } from "react-router-dom";
import styles from "./SidebarItem.module.scss";
import type { SidebarItemProps } from "./SidebarItem.types";
import Button from "../Button/Button";

const SidebarItem = ({ label, path, onClick }: SidebarItemProps) => {

  // Navbar for navigation
  if (path) {
    return (
      <NavLink to={path} className={styles.sideBarItem} end>
        {label}
      </NavLink>
    );
  }

  // For logout api
  return (
    <Button type="button" onClick={onClick} className={styles.sideBarItem}>
      {label}
    </Button>
  );
};

export default SidebarItem;