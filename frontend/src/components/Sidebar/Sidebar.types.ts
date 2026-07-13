export interface SidebarLink {
  label: string;
  path: string;
}

export interface SidebarProps {
  user: string;
  links: SidebarLink[];
  onLogout: () => void;
}