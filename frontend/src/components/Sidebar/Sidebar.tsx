import SidebarItem from "../SidebarItem/SidebarItem";
import styles from "./Sidebar.module.scss";
import type { SidebarProps } from "./Sidebar.types";

const Sidebar = ({ user, links, onLogout }: SidebarProps) => {
  return (
    <section className={styles.background}>
      <div className={styles.header}>
        <h3>Hello, {user} !</h3>
      </div>

      <nav className={styles.navLinks}>
        {links.map((link) => (
          <SidebarItem 
            key={link.path} 
            label={link.label} 
            path={link.path} 
          />
        ))}
      </nav>

      <div className={styles.logoutSection}>
        <SidebarItem label="Logout" onClick={onLogout} />
      </div>
    </section>
  );
};

export default Sidebar;