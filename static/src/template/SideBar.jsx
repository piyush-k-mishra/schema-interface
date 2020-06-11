import React, { Component } from "react";

class SideBar extends Component {
    render() {
        const sidebarClass = this.props.isOpen ? 'sidebar open' : 'sidebar'
        return (
            <div className={sidebarClass}>
                <div>Slider here.</div>
                <button onClick={this.props.toggleSidebar} className="sidebar-toggle">Toggle Sidebar</button>
            </div>
        );
    }
}

export default SideBar;