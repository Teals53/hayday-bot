from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                             QComboBox, QPushButton, QLabel, QLineEdit, 
                             QSpinBox, QMessageBox, QInputDialog, QGridLayout,
                             QFormLayout, QScrollArea, QDoubleSpinBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from .field_selector_popup import FieldSelectorPopup
from core.screenshot_service import ScreenshotManager

class FarmConfigTab(QWidget):
    config_changed = pyqtSignal(str)
    
    def __init__(self, bot_core):
        super().__init__()
        self.bot_core = bot_core
        self.current_config_name = None
        self.current_config_data = None
        self.current_field_polygon = None  # Store polygon data for saving
        
        # Create screenshot manager for field selection
        self.screenshot_manager = ScreenshotManager(bot_core)
        self.screenshot_manager.screenshot_taken.connect(self.on_field_screenshot_taken)
        self.screenshot_manager.status_message.connect(self.show_status_message)
        self.pending_field_selection = False
        
        self.init_ui()
    
    def cleanup(self):
        """Cleanup resources when tab is closed"""
        if hasattr(self, 'screenshot_manager') and self.screenshot_manager.worker:
            if self.screenshot_manager.worker.isRunning():
                self.screenshot_manager.worker.quit()
                self.screenshot_manager.worker.wait()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(8)  # Reduce spacing between main sections
        layout.setContentsMargins(5, 5, 5, 5)  # Reduce margins
        
        # Config Selection Group
        config_group = QGroupBox("Configuration Selection")
        config_layout = QVBoxLayout()
        config_layout.setSpacing(8)  # Reduce spacing
        config_layout.setContentsMargins(10, 10, 10, 10)  # Reduce margins
        
        # Config selection row
        config_select_layout = QHBoxLayout()
        config_select_layout.setSpacing(5)  # Reduce spacing between elements
        config_select_layout.addWidget(QLabel("Current Config:"))
        
        self.config_combo = QComboBox()
        self.config_combo.setMinimumWidth(200)
        self.config_combo.currentTextChanged.connect(self.on_config_selected)
        config_select_layout.addWidget(self.config_combo)
        
        self.refresh_configs_btn = QPushButton("Refresh")
        self.refresh_configs_btn.clicked.connect(self.refresh_configs)
        config_select_layout.addWidget(self.refresh_configs_btn)
        
        config_layout.addLayout(config_select_layout)
        
        # Config management buttons
        config_buttons_layout = QHBoxLayout()
        config_buttons_layout.setSpacing(5)  # Reduce spacing between buttons
        
        self.add_config_btn = QPushButton("Add Config")
        self.add_config_btn.clicked.connect(self.add_new_config)
        config_buttons_layout.addWidget(self.add_config_btn)
        
        self.delete_config_btn = QPushButton("Delete Config")
        self.delete_config_btn.clicked.connect(self.delete_config)
        config_buttons_layout.addWidget(self.delete_config_btn)
        
        self.save_config_btn = QPushButton("Save Config")
        self.save_config_btn.clicked.connect(self.save_config)
        self.save_config_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
        config_buttons_layout.addWidget(self.save_config_btn)
        
        config_layout.addLayout(config_buttons_layout)
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Scrollable area for config details
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setSpacing(8)  # Reduce spacing between groups
        scroll_layout.setContentsMargins(5, 5, 5, 5)  # Reduce margins
        
        # Create horizontal layout for the first row of sections
        first_row_layout = QHBoxLayout()
        first_row_layout.setSpacing(15)
        
        # Field Zone Group - with editable coordinates
        field_group = QGroupBox("Field Zone")
        field_layout = QVBoxLayout()
        field_layout.setSpacing(8)
        field_layout.setContentsMargins(12, 12, 12, 12)
        
        # Initialize coordinate spinboxes for 4 points
        self.field_coord_spins = []
        for i in range(4):
            coord_row = QHBoxLayout()
            coord_row.setSpacing(8)
            
            # Point label
            point_label = QLabel(f"P{i+1}:")
            point_label.setMinimumWidth(25)
            point_label.setMaximumWidth(25)
            coord_row.addWidget(point_label)
            
            # X coordinate
            coord_row.addWidget(QLabel("X:"))
            x_spin = QSpinBox()
            x_spin.setRange(-9999, 9999)
            x_spin.setValue(0)
            x_spin.setMinimumWidth(60)
            x_spin.setMaximumWidth(60)
            coord_row.addWidget(x_spin)
            
            # Y coordinate
            coord_row.addWidget(QLabel("Y:"))
            y_spin = QSpinBox()
            y_spin.setRange(-9999, 9999)
            y_spin.setValue(0)
            y_spin.setMinimumWidth(60)
            y_spin.setMaximumWidth(60)
            coord_row.addWidget(y_spin)
            
            # Store the spinboxes
            self.field_coord_spins.append((x_spin, y_spin))
            
            field_layout.addLayout(coord_row)
        
        # Select field area button
        self.select_field_btn = QPushButton("Select Field")
        self.select_field_btn.clicked.connect(self.open_field_selector)
        self.select_field_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; }")
        field_layout.addWidget(self.select_field_btn)
        
        field_group.setLayout(field_layout)
        field_group.setMaximumWidth(250)
        first_row_layout.addWidget(field_group)
        
        # Navigation Decoration Group - more compact
        nav_group = QGroupBox("Navigation Decoration")
        nav_layout = QVBoxLayout()
        nav_layout.setSpacing(8)
        nav_layout.setContentsMargins(12, 12, 12, 12)
        
        # Decoration selection - compact
        dec_row1 = QHBoxLayout()
        dec_row1.setSpacing(15)
        dec_row1.addWidget(QLabel("Decoration:"))
        self.decoration_combo = QComboBox()
        self.decoration_combo.setMinimumWidth(120)
        self.decoration_combo.setMaximumWidth(120)
        dec_row1.addWidget(self.decoration_combo)
        
        # Add some space between combo and button
        dec_row1.addSpacing(40)
        
        self.refresh_decorations_btn = QPushButton("Refresh")
        self.refresh_decorations_btn.clicked.connect(self.refresh_decorations)
        self.refresh_decorations_btn.setMinimumWidth(80)
        self.refresh_decorations_btn.setMaximumWidth(80)
        dec_row1.addWidget(self.refresh_decorations_btn)
        nav_layout.addLayout(dec_row1)
        
        # Decoration offset - compact
        dec_row2 = QHBoxLayout()
        dec_row2.setSpacing(15)
        dec_row2.addWidget(QLabel("Decoration Offset:"))
        self.decoration_offset_spin = QSpinBox()
        self.decoration_offset_spin.setRange(-9999, 9999)
        self.decoration_offset_spin.setValue(0)
        self.decoration_offset_spin.setMinimumWidth(80)
        self.decoration_offset_spin.setMaximumWidth(80)
        dec_row2.addWidget(self.decoration_offset_spin)
        nav_layout.addLayout(dec_row2)
        
        nav_group.setLayout(nav_layout)
        nav_group.setMaximumWidth(300)
        first_row_layout.addWidget(nav_group)
        
        # Tool Offsets Group - more compact
        tool_group = QGroupBox("Tool Offsets")
        tool_layout = QVBoxLayout()
        tool_layout.setSpacing(8)
        tool_layout.setContentsMargins(12, 12, 12, 12)
        
        # Plant offset - compact with proper alignment
        plant_row = QHBoxLayout()
        plant_row.setSpacing(8)
        
        # Create a label with fixed width for alignment
        plant_label = QLabel("Plant Offset:")
        plant_label.setMinimumWidth(100)
        plant_label.setMaximumWidth(100)
        plant_row.addWidget(plant_label)
        
        plant_row.addSpacing(10)
        plant_row.addWidget(QLabel("X:"))
        self.plant_x_spin = QSpinBox()
        self.plant_x_spin.setRange(-9999, 9999)
        self.plant_x_spin.setValue(0)
        self.plant_x_spin.setMinimumWidth(80)
        self.plant_x_spin.setMaximumWidth(80)
        plant_row.addWidget(self.plant_x_spin)
        
        plant_row.addSpacing(10)
        plant_row.addWidget(QLabel("Y:"))
        self.plant_y_spin = QSpinBox()
        self.plant_y_spin.setRange(-9999, 9999)
        self.plant_y_spin.setValue(0)
        self.plant_y_spin.setMinimumWidth(80)
        self.plant_y_spin.setMaximumWidth(80)
        plant_row.addWidget(self.plant_y_spin)
        tool_layout.addLayout(plant_row)
        
        # Harvest offset - compact with proper alignment
        harvest_row = QHBoxLayout()
        harvest_row.setSpacing(8)
        
        # Create a label with fixed width for alignment
        harvest_label = QLabel("Harvest Offset:")
        harvest_label.setMinimumWidth(100)
        harvest_label.setMaximumWidth(100)
        harvest_row.addWidget(harvest_label)
        
        harvest_row.addSpacing(10)
        harvest_row.addWidget(QLabel("X:"))
        self.harvest_x_spin = QSpinBox()
        self.harvest_x_spin.setRange(-9999, 9999)
        self.harvest_x_spin.setValue(0)
        self.harvest_x_spin.setMinimumWidth(80)
        self.harvest_x_spin.setMaximumWidth(80)
        harvest_row.addWidget(self.harvest_x_spin)
        
        harvest_row.addSpacing(10)
        harvest_row.addWidget(QLabel("Y:"))
        self.harvest_y_spin = QSpinBox()
        self.harvest_y_spin.setRange(-9999, 9999)
        self.harvest_y_spin.setValue(0)
        self.harvest_y_spin.setMinimumWidth(80)
        self.harvest_y_spin.setMaximumWidth(80)
        harvest_row.addWidget(self.harvest_y_spin)
        tool_layout.addLayout(harvest_row)
        
        tool_group.setLayout(tool_layout)
        tool_group.setMaximumWidth(350)
        first_row_layout.addWidget(tool_group)
        
        # Price Settings Group - more compact
        price_group = QGroupBox("Price Settings")
        price_layout = QVBoxLayout()
        price_layout.setSpacing(8)
        price_layout.setContentsMargins(12, 12, 12, 12)
        
        # Price option selection - compact
        price_row = QHBoxLayout()
        price_row.setSpacing(15)
        price_row.addWidget(QLabel("Price Option:"))
        self.price_option_combo = QComboBox()
        self.price_option_combo.addItems(["low", "mid", "high"])
        self.price_option_combo.setCurrentText("high")
        self.price_option_combo.setMinimumWidth(80)
        self.price_option_combo.setMaximumWidth(80)
        price_row.addWidget(self.price_option_combo)
        price_layout.addLayout(price_row)
        
        # Add description - compact
        price_desc = QLabel("Low: ← | Mid: Skip | High: →")
        price_desc.setStyleSheet("QLabel { color: #666; }")
        price_layout.addWidget(price_desc)
        
        price_group.setLayout(price_layout)
        price_group.setMaximumWidth(200)
        first_row_layout.addWidget(price_group)
        
        # Add stretch to center the first section
        first_row_layout.addStretch()
        
        # Create a container to center the first row
        first_row_container = QHBoxLayout()
        first_row_container.addStretch()
        first_row_container.addLayout(first_row_layout)
        first_row_container.addStretch()
        
        scroll_layout.addLayout(first_row_container)
        
        # Template Thresholds Section
        thresholds_group = QGroupBox("Template Thresholds")
        thresholds_layout = QVBoxLayout()
        
        # Individual template thresholds organized by category
        self.template_thresholds = {}
        self.refresh_template_thresholds(thresholds_layout)
        
        thresholds_group.setLayout(thresholds_layout)
        
        # Create a container to center the template thresholds section
        thresholds_container = QHBoxLayout()
        thresholds_container.addStretch()
        thresholds_container.addWidget(thresholds_group)
        thresholds_container.addStretch()
        
        scroll_layout.addLayout(thresholds_container)
        
        # Experimental Settings Toggle Button
        experimental_button_layout = QHBoxLayout()
        experimental_button_layout.addStretch()  # Center the button
        
        self.experimental_toggle_btn = QPushButton("Show Experimental Settings")
        self.experimental_toggle_btn.setCheckable(True)
        self.experimental_toggle_btn.setChecked(False)
        self.experimental_toggle_btn.clicked.connect(self.toggle_experimental_settings)
        self.experimental_toggle_btn.setStyleSheet("QPushButton { background-color: #FF9800; color: white; font-weight: bold; }")
        
        experimental_button_layout.addWidget(self.experimental_toggle_btn)
        experimental_button_layout.addStretch()  # Center the button
        
        # Create a widget for the button layout
        experimental_button_widget = QWidget()
        experimental_button_widget.setLayout(experimental_button_layout)
        scroll_layout.addWidget(experimental_button_widget)
        
        # Create horizontal layout for experimental settings
        experimental_row_layout = QHBoxLayout()
        experimental_row_layout.setSpacing(15)
        
        # Market Timing Settings Group - Two column layout
        self.timing_group = QGroupBox("Market Speed Settings")
        timing_layout = QVBoxLayout()
        timing_layout.setSpacing(8)
        timing_layout.setContentsMargins(12, 12, 12, 12)
        
        # Market cycle interval
        market_row = QHBoxLayout()
        market_row.setSpacing(15)
        market_row.addWidget(QLabel("Market Check Interval:"))
        self.market_interval_spin = QSpinBox()
        self.market_interval_spin.setRange(5, 30)
        self.market_interval_spin.setValue(10)
        self.market_interval_spin.setSuffix(" seconds")
        self.market_interval_spin.setMinimumWidth(90)
        self.market_interval_spin.setMaximumWidth(90)
        market_row.addWidget(self.market_interval_spin)
        timing_layout.addLayout(market_row)
        
        # Timing presets
        preset_row = QHBoxLayout()
        preset_row.setSpacing(15)
        preset_row.addWidget(QLabel("Timing Preset:"))
        self.timing_preset_combo = QComboBox()
        self.timing_preset_combo.addItems(["Fast", "Normal", "Safe", "Custom"])
        self.timing_preset_combo.setCurrentText("Fast")
        self.timing_preset_combo.currentTextChanged.connect(self.on_timing_preset_changed)
        self.timing_preset_combo.setMinimumWidth(90)
        self.timing_preset_combo.setMaximumWidth(90)
        preset_row.addWidget(self.timing_preset_combo)
        timing_layout.addLayout(preset_row)
        
        # Individual timing controls - two column layout
        self.timing_controls = {}
        timing_descriptions = {
            'escape_wait': 'Escape Wait',
            'market_open_wait': 'Market Open Wait',
            'collection_wait': 'Collection Wait',
            'offer_page_wait': 'Offer Page Wait',
            'quantity_click_delay': 'Quantity Click Delay',
            'price_set_wait': 'Price Set Wait',
            'offer_create_wait': 'Offer Create Wait',
            'page_close_wait': 'Page Close Wait',
            'verification_wait': 'Verification Wait',
            'advert_page_wait': 'Advertisement Page Wait'
        }
        
        # Create two column layout for timing controls
        timing_columns_layout = QHBoxLayout()
        timing_columns_layout.setSpacing(20)
        
        # Left column
        left_column = QVBoxLayout()
        left_column.setSpacing(8)
        
        # Right column
        right_column = QVBoxLayout()
        right_column.setSpacing(8)
        
        timing_items = list(timing_descriptions.items())
        for i, (key, description) in enumerate(timing_items):
            timing_control_row = QHBoxLayout()
            timing_control_row.setSpacing(15)
            
            label = QLabel(f"{description}:")
            label.setMinimumWidth(140)
            label.setMaximumWidth(140)
            timing_control_row.addWidget(label)
            
            spin = QDoubleSpinBox()
            spin.setRange(0.1, 5.0)
            spin.setSingleStep(0.1)
            spin.setSuffix(" seconds")
            spin.setDecimals(1)
            spin.setMinimumWidth(90)
            spin.setMaximumWidth(90)
            timing_control_row.addWidget(spin)
            self.timing_controls[key] = spin
            
            # Alternate between left and right columns
            if i % 2 == 0:
                left_column.addLayout(timing_control_row)
            else:
                right_column.addLayout(timing_control_row)
        
        # Max verification attempts - add to right column
        attempts_row = QHBoxLayout()
        attempts_row.setSpacing(15)
        attempts_label = QLabel("Max Verification Attempts:")
        attempts_label.setMinimumWidth(140)
        attempts_label.setMaximumWidth(140)
        attempts_row.addWidget(attempts_label)
        self.max_attempts_spin = QSpinBox()
        self.max_attempts_spin.setRange(1, 5)
        self.max_attempts_spin.setValue(2)
        self.max_attempts_spin.setMinimumWidth(90)
        self.max_attempts_spin.setMaximumWidth(90)
        attempts_row.addWidget(self.max_attempts_spin)
        self.timing_controls['max_verification_attempts'] = self.max_attempts_spin
        right_column.addLayout(attempts_row)
        
        timing_columns_layout.addLayout(left_column)
        timing_columns_layout.addLayout(right_column)
        timing_layout.addLayout(timing_columns_layout)
        
        self.timing_group.setLayout(timing_layout)
        self.timing_group.setMaximumWidth(600)
        experimental_row_layout.addWidget(self.timing_group)
        
        # Farming Timing Group - Two column layout
        self.farming_timing_group = QGroupBox("Farming Speed Settings")
        farming_layout = QVBoxLayout()
        farming_layout.setSpacing(8)
        farming_layout.setContentsMargins(12, 12, 12, 12)
        
        # Initialize farming timing controls dictionary
        self.farming_timing_controls = {}
        
        # Wheat growth time
        wheat_row = QHBoxLayout()
        wheat_row.setSpacing(15)
        wheat_row.addWidget(QLabel("Wheat Growth Time:"))
        wheat_growth_spin = QDoubleSpinBox()
        wheat_growth_spin.setRange(30.0, 600.0)
        wheat_growth_spin.setSuffix(" seconds")
        wheat_growth_spin.setDecimals(0)
        wheat_growth_spin.setMinimumWidth(90)
        wheat_growth_spin.setMaximumWidth(90)
        wheat_row.addWidget(wheat_growth_spin)
        self.farming_timing_controls['wheat_growth_time'] = wheat_growth_spin
        farming_layout.addLayout(wheat_row)
        
        # Farming speed presets
        farming_preset_row = QHBoxLayout()
        farming_preset_row.setSpacing(15)
        farming_preset_row.addWidget(QLabel("Farming Speed Preset:"))
        self.farming_preset_combo = QComboBox()
        self.farming_preset_combo.addItems(["Lightning", "Fast", "Normal", "Safe", "Custom"])
        self.farming_preset_combo.setCurrentText("Fast")
        self.farming_preset_combo.currentTextChanged.connect(self.on_farming_preset_changed)
        self.farming_preset_combo.setMinimumWidth(90)
        self.farming_preset_combo.setMaximumWidth(90)
        farming_preset_row.addWidget(self.farming_preset_combo)
        farming_layout.addLayout(farming_preset_row)
        
        # Create two column layout for farming controls
        farming_columns_layout = QHBoxLayout()
        farming_columns_layout.setSpacing(20)
        
        # Left column
        farming_left_column = QVBoxLayout()
        farming_left_column.setSpacing(8)
        
        # Right column
        farming_right_column = QVBoxLayout()
        farming_right_column.setSpacing(8)
        
        # Basic farming timing controls - two column layout
        basic_farming_descriptions = {
            'post_plant_delay': 'Post Plant Delay',
            'field_recenter_wait': 'Field Recenter Wait',
            'popup_close_wait': 'Popup Close Wait',
            'main_screen_retry_wait': 'Main Screen Retry Wait',
            'cycle_error_wait': 'Cycle Error Wait',
            'silo_popup_wait': 'Silo Popup Wait',
            'screenshot_retry_wait': 'Screenshot Retry Wait',
            'market_check_interval': 'Market Check Interval'
        }
        
        farming_items = list(basic_farming_descriptions.items())
        for i, (key, description) in enumerate(farming_items):
            farming_control_row = QHBoxLayout()
            farming_control_row.setSpacing(15)
            
            label = QLabel(f"{description}:")
            label.setMinimumWidth(140)
            label.setMaximumWidth(140)
            farming_control_row.addWidget(label)
            
            spin = QDoubleSpinBox()
            spin.setRange(0.1, 10.0)
            spin.setSuffix(" seconds")
            spin.setSingleStep(0.1)
            spin.setDecimals(1)
            spin.setMinimumWidth(90)
            spin.setMaximumWidth(90)
            farming_control_row.addWidget(spin)
            self.farming_timing_controls[key] = spin
            
            # Alternate between left and right columns
            if i % 2 == 0:
                farming_left_column.addLayout(farming_control_row)
            else:
                farming_right_column.addLayout(farming_control_row)
        
        # Detection area settings - add to columns
        detection_width_row = QHBoxLayout()
        detection_width_row.setSpacing(15)
        width_label = QLabel("Detection Area Width:")
        width_label.setMinimumWidth(140)
        width_label.setMaximumWidth(140)
        detection_width_row.addWidget(width_label)
        detection_area_width_spin = QSpinBox()
        detection_area_width_spin.setRange(30, 200)
        detection_area_width_spin.setSuffix(" pixels")
        detection_area_width_spin.setMinimumWidth(90)
        detection_area_width_spin.setMaximumWidth(90)
        detection_width_row.addWidget(detection_area_width_spin)
        self.farming_timing_controls['detection_area_width'] = detection_area_width_spin
        farming_left_column.addLayout(detection_width_row)
        
        detection_height_row = QHBoxLayout()
        detection_height_row.setSpacing(15)
        height_label = QLabel("Detection Area Height:")
        height_label.setMinimumWidth(140)
        height_label.setMaximumWidth(140)
        detection_height_row.addWidget(height_label)
        detection_area_height_spin = QSpinBox()
        detection_area_height_spin.setRange(30, 200)
        detection_area_height_spin.setSuffix(" pixels")
        detection_area_height_spin.setMinimumWidth(90)
        detection_area_height_spin.setMaximumWidth(90)
        detection_height_row.addWidget(detection_area_height_spin)
        self.farming_timing_controls['detection_area_height'] = detection_area_height_spin
        farming_right_column.addLayout(detection_height_row)
        
        path_spacing_row = QHBoxLayout()
        path_spacing_row.setSpacing(15)
        spacing_label = QLabel("Path Spacing:")
        spacing_label.setMinimumWidth(140)
        spacing_label.setMaximumWidth(140)
        path_spacing_row.addWidget(spacing_label)
        path_spacing_spin = QSpinBox()
        path_spacing_spin.setRange(20, 100)
        path_spacing_spin.setSuffix(" pixels")
        path_spacing_spin.setMinimumWidth(90)
        path_spacing_spin.setMaximumWidth(90)
        path_spacing_row.addWidget(path_spacing_spin)
        self.farming_timing_controls['path_spacing'] = path_spacing_spin
        farming_left_column.addLayout(path_spacing_row)
        
        path_random_row = QHBoxLayout()
        path_random_row.setSpacing(15)
        random_label = QLabel("Path Randomization:")
        random_label.setMinimumWidth(140)
        random_label.setMaximumWidth(140)
        path_random_row.addWidget(random_label)
        path_randomization_spin = QSpinBox()
        path_randomization_spin.setRange(0, 10)
        path_randomization_spin.setSuffix(" pixels")
        path_randomization_spin.setMinimumWidth(90)
        path_randomization_spin.setMaximumWidth(90)
        path_random_row.addWidget(path_randomization_spin)
        self.farming_timing_controls['path_randomization_pixels'] = path_randomization_spin
        farming_right_column.addLayout(path_random_row)
        
        drag_duration_row = QHBoxLayout()
        drag_duration_row.setSpacing(15)
        drag_label = QLabel("Continuous Drag Duration:")
        drag_label.setMinimumWidth(140)
        drag_label.setMaximumWidth(140)
        drag_duration_row.addWidget(drag_label)
        continuous_drag_spin = QSpinBox()
        continuous_drag_spin.setRange(10, 200)
        continuous_drag_spin.setSuffix(" ms")
        continuous_drag_spin.setMinimumWidth(90)
        continuous_drag_spin.setMaximumWidth(90)
        drag_duration_row.addWidget(continuous_drag_spin)
        self.farming_timing_controls['continuous_drag_duration_per_segment'] = continuous_drag_spin
        farming_left_column.addLayout(drag_duration_row)
        
        farming_columns_layout.addLayout(farming_left_column)
        farming_columns_layout.addLayout(farming_right_column)
        farming_layout.addLayout(farming_columns_layout)
        
        self.farming_timing_group.setLayout(farming_layout)
        self.farming_timing_group.setMaximumWidth(650)
        experimental_row_layout.addWidget(self.farming_timing_group)
        
        # Add stretch to center the experimental sections
        experimental_row_layout.addStretch()
        
        # Create a container to center the experimental row
        experimental_container = QHBoxLayout()
        experimental_container.addStretch()
        experimental_container.addLayout(experimental_row_layout)
        experimental_container.addStretch()
        
        scroll_layout.addLayout(experimental_container)
        
        scroll_layout.addStretch()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        self.setLayout(layout)
        
        # Initialize data
        self.refresh_configs()
        self.refresh_decorations()
        
        # Initially hide experimental settings
        self.timing_group.setVisible(False)
        self.farming_timing_group.setVisible(False)
        
        # Connect change signals
        self.connect_change_signals()
    
    def connect_change_signals(self):
        """Connect signals to detect configuration changes"""
        # Connect field coordinate change signals
        for x_spin, y_spin in self.field_coord_spins:
            x_spin.valueChanged.connect(self.on_config_changed)
            y_spin.valueChanged.connect(self.on_config_changed)
        
        self.decoration_combo.currentTextChanged.connect(self.on_config_changed)
        self.decoration_offset_spin.valueChanged.connect(self.on_config_changed)
        self.harvest_x_spin.valueChanged.connect(self.on_config_changed)
        self.harvest_y_spin.valueChanged.connect(self.on_config_changed)
        self.plant_x_spin.valueChanged.connect(self.on_config_changed)
        self.plant_y_spin.valueChanged.connect(self.on_config_changed)
        self.price_option_combo.currentTextChanged.connect(self.on_config_changed)
        self.market_interval_spin.valueChanged.connect(self.on_config_changed)
        # Preset combos are handled separately (they trigger updates to timing controls)
        self.timing_preset_combo.currentTextChanged.connect(self.on_timing_preset_changed)
        self.farming_preset_combo.currentTextChanged.connect(self.on_farming_preset_changed)
        for control in self.timing_controls.values():
            control.valueChanged.connect(self.on_config_changed)
        for control in self.farming_timing_controls.values():
            control.valueChanged.connect(self.on_config_changed)
        for template_name, spin in self.template_thresholds.items():
            spin.valueChanged.connect(self.on_config_changed)
    
    def refresh_configs(self):
        """Refresh the list of available configurations"""
        configs = self.bot_core.config_manager.get_config_names()
        self.config_combo.clear()
        
        if configs:
            self.config_combo.addItems(configs)
        else:
            self.config_combo.addItem("No configurations found")
    
    def refresh_decorations(self):
        """Refresh the list of available decorations"""
        decorations = self.bot_core.template_detector.get_decorations()
        self.decoration_combo.clear()
        
        if decorations:
            self.decoration_combo.addItems(decorations)
        else:
            self.decoration_combo.addItem("No decorations found")
    
    def on_config_selected(self, config_name: str):
        """Handle configuration selection"""
        if not config_name or config_name == "No configurations found":
            return
        
        self.current_config_name = config_name
        self.load_config_data(config_name)
        
        # Set as current config in bot core
        self.bot_core.set_current_config(config_name)
    
    def load_config_data(self, config_name: str):
        """Load configuration data into UI"""
        config_data = self.bot_core.config_manager.load_config(config_name)
        
        if not config_data:
            QMessageBox.warning(self, "Error", f"Failed to load configuration: {config_name}")
            return
        
        self.current_config_data = config_data
        
        # Disconnect signals temporarily to avoid triggering changes
        self.disconnect_change_signals()
        
        try:
            # Load field zone polygon data
            field_zone = config_data.get('field_zone', {})
            self.current_field_polygon = field_zone.get('polygon', None)
            
            # Load coordinates into spinboxes
            if self.current_field_polygon and len(self.current_field_polygon) == 4:
                for i, (x, y) in enumerate(self.current_field_polygon):
                    if i < len(self.field_coord_spins):
                        x_spin, y_spin = self.field_coord_spins[i]
                        x_spin.setValue(x)
                        y_spin.setValue(y)
            else:
                # Reset all coordinates to 0 if no valid polygon
                for x_spin, y_spin in self.field_coord_spins:
                    x_spin.setValue(0)
                    y_spin.setValue(0)
            
            # Load navigation decoration
            nav_deco = config_data.get('navigation_decoration', {})
            decoration = nav_deco.get('decoration', '')
            if decoration and decoration in [self.decoration_combo.itemText(i) for i in range(self.decoration_combo.count())]:
                self.decoration_combo.setCurrentText(decoration)
            self.decoration_offset_spin.setValue(nav_deco.get('offset'))
            
            # Load tool offsets
            tool_offsets = config_data.get('tool_offsets', {})
            harvest_offset = tool_offsets.get('harvest')
            plant_offset = tool_offsets.get('plant')
            
            if harvest_offset:
                self.harvest_x_spin.setValue(harvest_offset.get('x'))
                self.harvest_y_spin.setValue(harvest_offset.get('y'))
            if plant_offset:
                self.plant_x_spin.setValue(plant_offset.get('x'))
                self.plant_y_spin.setValue(plant_offset.get('y'))
            
            # Load price settings
            price_settings = config_data.get('price_settings', {})
            price_option = price_settings.get('price_option', 'high')
            self.price_option_combo.setCurrentText(price_option)
            
            # Load market timing settings
            market_timing = config_data.get('market_timing', {})
            for key, control in self.timing_controls.items():
                if key in market_timing:
                    control.setValue(market_timing[key])
            
            # Load farming timing settings
            farming_timing = config_data.get('farming_timing', {})
            for key, control in self.farming_timing_controls.items():
                if key in farming_timing:
                    control.setValue(farming_timing[key])
            
            # Load cycle settings
            cycle_settings = config_data.get('cycle_settings', {})
            market_interval = cycle_settings.get('market_cycle_interval', 10)
            self.market_interval_spin.setValue(market_interval)
            
            # Load template thresholds
            template_thresholds = config_data.get('template_thresholds', {})
            for template_name, threshold in template_thresholds.get('templates', {}).items():
                if template_name in self.template_thresholds:
                    self.template_thresholds[template_name].setValue(threshold)
                    self.template_thresholds[template_name].setEnabled(True)
            
        finally:
            # Reconnect signals
            self.connect_change_signals()
    
    def disconnect_change_signals(self):
        """Temporarily disconnect change signals"""
        # Disconnect field coordinate change signals
        for x_spin, y_spin in self.field_coord_spins:
            try:
                x_spin.valueChanged.disconnect(self.on_config_changed)
            except TypeError:
                pass
            try:
                y_spin.valueChanged.disconnect(self.on_config_changed)
            except TypeError:
                pass
        
        try:
            self.decoration_combo.currentTextChanged.disconnect(self.on_config_changed)
        except TypeError:
            pass
        try:
            self.decoration_offset_spin.valueChanged.disconnect(self.on_config_changed)
        except TypeError:
            pass
        try:
            self.harvest_x_spin.valueChanged.disconnect(self.on_config_changed)
        except TypeError:
            pass
        try:
            self.harvest_y_spin.valueChanged.disconnect(self.on_config_changed)
        except TypeError:
            pass
        try:
            self.plant_x_spin.valueChanged.disconnect(self.on_config_changed)
        except TypeError:
            pass
        try:
            self.plant_y_spin.valueChanged.disconnect(self.on_config_changed)
        except TypeError:
            pass
        try:
            self.price_option_combo.currentTextChanged.disconnect(self.on_config_changed)
        except TypeError:
            pass
        try:
            self.market_interval_spin.valueChanged.disconnect(self.on_config_changed)
        except TypeError:
            pass
        # Disconnect preset combos
        try:
            self.timing_preset_combo.currentTextChanged.disconnect(self.on_timing_preset_changed)
        except TypeError:
            pass
        try:
            self.farming_preset_combo.currentTextChanged.disconnect(self.on_farming_preset_changed)
        except TypeError:
            pass
        for control in self.timing_controls.values():
            try:
                control.valueChanged.disconnect(self.on_config_changed)
            except TypeError:
                pass
        for control in self.farming_timing_controls.values():
            try:
                control.valueChanged.disconnect(self.on_config_changed)
            except TypeError:
                pass
        for template_name, spin in self.template_thresholds.items():
            try:
                spin.valueChanged.disconnect(self.on_config_changed)
            except TypeError:
                pass
    
    def on_timing_preset_changed(self, preset: str):
        """Handle timing preset changes"""
        timing_presets = {
            "Fast": {
                'escape_wait': 0.3,
                'market_open_wait': 0.8,
                'collection_wait': 0.2,
                'offer_page_wait': 0.8,
                'quantity_click_delay': 0.1,
                'price_set_wait': 0.3,
                'offer_create_wait': 0.8,
                'page_close_wait': 0.2,
                'verification_wait': 0.3,
                'advert_page_wait': 0.8,
                'max_verification_attempts': 2
            },
            "Normal": {
                'escape_wait': 0.5,
                'market_open_wait': 1.0,
                'collection_wait': 0.3,
                'offer_page_wait': 1.0,
                'quantity_click_delay': 0.2,
                'price_set_wait': 0.5,
                'offer_create_wait': 1.0,
                'page_close_wait': 0.3,
                'verification_wait': 0.5,
                'advert_page_wait': 1.0,
                'max_verification_attempts': 2
            },
            "Safe": {
                'escape_wait': 1.0,
                'market_open_wait': 2.0,
                'collection_wait': 1.0,
                'offer_page_wait': 2.0,
                'quantity_click_delay': 0.5,
                'price_set_wait': 1.0,
                'offer_create_wait': 2.0,
                'page_close_wait': 1.0,
                'verification_wait': 1.0,
                'advert_page_wait': 2.0,
                'max_verification_attempts': 3
            }
        }
        
        if preset in timing_presets:
            values = timing_presets[preset]
            for key, value in values.items():
                if key in self.timing_controls:
                    self.timing_controls[key].setValue(value)
    
    def on_farming_preset_changed(self, preset: str):
        """Handle farming preset changes"""
        # Store current wheat growth time
        current_growth_time = self.farming_timing_controls['wheat_growth_time'].value()
        
        farming_presets = {
            "Lightning": {
                'post_plant_delay': 0.5,
                'field_recenter_wait': 0.5,
                'popup_close_wait': 0.3,
                'main_screen_retry_wait': 0.5,
                'cycle_error_wait': 1.0,
                'silo_popup_wait': 0.3,
                'screenshot_retry_wait': 0.5,
                'market_check_interval': 0.5,
                'harvest_start_delay_min': 0.05,
                'harvest_start_delay_max': 0.1,
                'harvest_tool_press_delay_min': 0.02,
                'harvest_tool_press_delay_max': 0.05,
                'harvest_move_delay_min': 0.02,
                'harvest_move_delay_max': 0.05,
                'harvest_field_move_delay_min': 0.02,
                'harvest_field_move_delay_max': 0.05,
                'plant_start_delay_min': 0.05,
                'plant_start_delay_max': 0.1,
                'plant_tool_press_delay_min': 0.02,
                'plant_tool_press_delay_max': 0.05,
                'plant_move_delay_min': 0.02,
                'plant_move_delay_max': 0.05,
                'plant_field_move_delay_min': 0.02,
                'plant_field_move_delay_max': 0.05,
                'path_randomization_pixels': 1,
                'continuous_drag_duration_per_segment': 30,
                'detection_area_width': 50,
                'detection_area_height': 50,
                'path_spacing': 25
            },
            "Fast": {
                'post_plant_delay': 1.0,
                'field_recenter_wait': 1.0,
                'popup_close_wait': 0.5,
                'main_screen_retry_wait': 1.0,
                'cycle_error_wait': 2.0,
                'silo_popup_wait': 0.5,
                'screenshot_retry_wait': 1.0,
                'market_check_interval': 1.0,
                'harvest_start_delay_min': 0.1,
                'harvest_start_delay_max': 0.3,
                'harvest_tool_press_delay_min': 0.05,
                'harvest_tool_press_delay_max': 0.1,
                'harvest_move_delay_min': 0.05,
                'harvest_move_delay_max': 0.1,
                'harvest_field_move_delay_min': 0.05,
                'harvest_field_move_delay_max': 0.1,
                'plant_start_delay_min': 0.1,
                'plant_start_delay_max': 0.3,
                'plant_tool_press_delay_min': 0.05,
                'plant_tool_press_delay_max': 0.1,
                'plant_move_delay_min': 0.05,
                'plant_move_delay_max': 0.1,
                'plant_field_move_delay_min': 0.05,
                'plant_field_move_delay_max': 0.1,
                'path_randomization_pixels': 2,
                'continuous_drag_duration_per_segment': 40,
                'detection_area_width': 70,
                'detection_area_height': 70,
                'path_spacing': 35
            },
            "Normal": {
                'post_plant_delay': 2.0,
                'field_recenter_wait': 1.5,
                'popup_close_wait': 1.0,
                'main_screen_retry_wait': 2.0,
                'cycle_error_wait': 5.0,
                'silo_popup_wait': 1.0,
                'screenshot_retry_wait': 2.0,
                'market_check_interval': 1.5,
                'harvest_start_delay_min': 0.3,
                'harvest_start_delay_max': 0.6,
                'harvest_tool_press_delay_min': 0.08,
                'harvest_tool_press_delay_max': 0.15,
                'harvest_move_delay_min': 0.08,
                'harvest_move_delay_max': 0.15,
                'harvest_field_move_delay_min': 0.08,
                'harvest_field_move_delay_max': 0.15,
                'plant_start_delay_min': 0.3,
                'plant_start_delay_max': 0.6,
                'plant_tool_press_delay_min': 0.08,
                'plant_tool_press_delay_max': 0.15,
                'plant_move_delay_min': 0.08,
                'plant_move_delay_max': 0.15,
                'plant_field_move_delay_min': 0.08,
                'plant_field_move_delay_max': 0.15,
                'path_randomization_pixels': 3,
                'continuous_drag_duration_per_segment': 50,
                'detection_area_width': 90,
                'detection_area_height': 90,
                'path_spacing': 45
            },
            "Safe": {
                'post_plant_delay': 3.0,
                'field_recenter_wait': 2.5,
                'popup_close_wait': 2.0,
                'main_screen_retry_wait': 3.0,
                'cycle_error_wait': 8.0,
                'silo_popup_wait': 2.0,
                'screenshot_retry_wait': 3.0,
                'market_check_interval': 2.0,
                'harvest_start_delay_min': 0.5,
                'harvest_start_delay_max': 1.0,
                'harvest_tool_press_delay_min': 0.15,
                'harvest_tool_press_delay_max': 0.25,
                'harvest_move_delay_min': 0.15,
                'harvest_move_delay_max': 0.25,
                'harvest_field_move_delay_min': 0.15,
                'harvest_field_move_delay_max': 0.25,
                'plant_start_delay_min': 0.5,
                'plant_start_delay_max': 1.0,
                'plant_tool_press_delay_min': 0.15,
                'plant_tool_press_delay_max': 0.25,
                'plant_move_delay_min': 0.15,
                'plant_move_delay_max': 0.25,
                'plant_field_move_delay_min': 0.15,
                'plant_field_move_delay_max': 0.25,
                'path_randomization_pixels': 5,
                'continuous_drag_duration_per_segment': 80,
                'detection_area_width': 120,
                'detection_area_height': 120,
                'path_spacing': 60
            }
        }
        
        if preset in farming_presets:
            values = farming_presets[preset]
            for key, value in values.items():
                if key in self.farming_timing_controls and key != 'wheat_growth_time':
                    self.farming_timing_controls[key].setValue(value)
            
            # Restore wheat growth time
            self.farming_timing_controls['wheat_growth_time'].setValue(current_growth_time)
    
    def on_config_changed(self):
        """Handle configuration changes"""
        # Configuration has changed - could trigger save prompt or auto-save here
        pass
    
    def toggle_experimental_settings(self):
        """Toggle visibility of experimental timing settings"""
        is_checked = self.experimental_toggle_btn.isChecked()
        
        # Toggle visibility of timing groups
        self.timing_group.setVisible(is_checked)
        self.farming_timing_group.setVisible(is_checked)
        
        # Update button text
        if is_checked:
            self.experimental_toggle_btn.setText("Hide Experimental Settings")
        else:
            self.experimental_toggle_btn.setText("Show Experimental Settings")
    
    def add_new_config(self):
        """Add a new configuration"""
        config_name, ok = QInputDialog.getText(self, "New Configuration", "Enter configuration name:")
        
        if ok and config_name:
            # Check if config already exists
            existing_configs = self.bot_core.config_manager.get_config_names()
            if config_name in existing_configs:
                QMessageBox.warning(self, "Error", "Configuration with this name already exists!")
                return
            
            # Create default config
            default_config = self.bot_core.config_manager.create_default_config(config_name)
            
            if self.bot_core.config_manager.save_config(config_name, default_config):
                self.refresh_configs()
                self.config_combo.setCurrentText(config_name)
                QMessageBox.information(self, "Success", f"Configuration '{config_name}' created successfully!")
            else:
                QMessageBox.warning(self, "Error", f"Failed to create configuration '{config_name}'")
    
    def delete_config(self):
        """Delete the current configuration"""
        if not self.current_config_name:
            QMessageBox.warning(self, "Warning", "No configuration selected!")
            return
        
        reply = QMessageBox.question(self, "Confirm Deletion", 
                                   f"Are you sure you want to delete configuration '{self.current_config_name}'?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.bot_core.config_manager.delete_config(self.current_config_name):
                self.current_config_name = None
                self.current_config_data = None
                self.refresh_configs()
                QMessageBox.information(self, "Success", "Configuration deleted successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to delete configuration")
    
    def save_config(self):
        """Save the current configuration"""
        if not self.current_config_name:
            QMessageBox.warning(self, "Warning", "No configuration selected!")
            return
        
        # Build config data from UI - get coordinates from spinboxes
        field_zone_data = {}
        
        # Get polygon data from coordinate spinboxes
        polygon_coords = []
        for x_spin, y_spin in self.field_coord_spins:
            polygon_coords.append((x_spin.value(), y_spin.value()))
        
        # Check if any coordinates are non-zero (valid polygon)
        if any(x != 0 or y != 0 for x, y in polygon_coords):
            field_zone_data['polygon'] = polygon_coords
            # Update stored polygon for consistency
            self.current_field_polygon = polygon_coords
        else:
            # No valid coordinates - configuration will fail validation
            field_zone_data['polygon'] = None
        
        config_data = {
            'field_zone': field_zone_data,
            'navigation_decoration': {
                'decoration': self.decoration_combo.currentText(),
                'offset': self.decoration_offset_spin.value()
            },
            'tool_offsets': {
                'harvest': {
                    'x': self.harvest_x_spin.value(),
                    'y': self.harvest_y_spin.value()
                },
                'plant': {
                    'x': self.plant_x_spin.value(),
                    'y': self.plant_y_spin.value()
                }
            },
            'detection_settings': {
                'detection_interval': 1.0
            },
            'template_thresholds': {
                'templates': {template_name: round(spin.value(), 2) for template_name, spin in self.template_thresholds.items()}
            },
            'game_settings': {
                'package_name': 'com.supercell.hayday',
                'wait_time_after_action': 2.0
            },
            'price_settings': {
                'price_option': self.price_option_combo.currentText()
            },
            'market_timing': {
                key: round(control.value(), 2) for key, control in self.timing_controls.items()
            },
            'farming_timing': {
                key: round(control.value(), 2) for key, control in self.farming_timing_controls.items()
            },
            'cycle_settings': {
                'market_cycle_interval': self.market_interval_spin.value()
            }
        }
        
        # Validate config
        errors = self.bot_core.config_manager.validate_config(config_data)
        if errors:
            QMessageBox.warning(self, "Validation Error", f"Configuration validation failed:\n{chr(10).join(errors)}")
            return
        
        # Save config
        if self.bot_core.config_manager.save_config(self.current_config_name, config_data):
            self.current_config_data = config_data
            # Update bot core config
            self.bot_core.set_current_config(self.current_config_name)
            QMessageBox.information(self, "Success", "Configuration saved successfully!")
        else:
            QMessageBox.warning(self, "Error", "Failed to save configuration")
    
    def open_field_selector(self):
        """Open field selector popup"""
        if not self.bot_core.adb_manager.is_connected():
            QMessageBox.warning(self, "Warning", "No device connected! Please connect a device first.")
            return
        
        # Set flag and take screenshot using service
        self.pending_field_selection = True
        self.screenshot_manager.take_single_screenshot()
    
    def on_field_screenshot_taken(self, screenshot):
        """Handle screenshot taken for field selection"""
        if not self.pending_field_selection:
            return
            
        self.pending_field_selection = False
        
        # Open field selector popup
        popup = FieldSelectorPopup(screenshot, self)
        if popup.exec() == popup.DialogCode.Accepted:
            field_polygon = popup.get_field_polygon()
            
            if field_polygon and len(field_polygon) == 4:
                # Store polygon data for later saving
                self.current_field_polygon = field_polygon
                
                # Update coordinate spinboxes
                for i, (x, y) in enumerate(field_polygon):
                    if i < len(self.field_coord_spins):
                        x_spin, y_spin = self.field_coord_spins[i]
                        x_spin.setValue(x)
                        y_spin.setValue(y)
                
                # Mark configuration as changed
                self.on_config_changed()
                
                # Calculate polygon bounds for display
                x_coords = [p[0] for p in field_polygon]
                y_coords = [p[1] for p in field_polygon]
                x1, x2 = min(x_coords), max(x_coords)
                y1, y2 = min(y_coords), max(y_coords)
                
                # Show success message with polygon info
                QMessageBox.information(self, "Success", 
                    f"Field polygon selected: 4-point shape\n"
                    f"Bounds: ({x1}, {y1}) to ({x2}, {y2})\n"
                    f"Area: {self._calculate_polygon_area(field_polygon):.0f} pixels")
    
    def show_status_message(self, message: str):
        """Show status message"""
        if "error" in message.lower() or "failed" in message.lower():
            QMessageBox.warning(self, "Screenshot Error", message)
            self.pending_field_selection = False
    
    def refresh_template_thresholds(self, parent_layout):
        """Create UI for individual template thresholds organized by category"""
        # Clear existing template threshold widgets
        for template_name, spin in self.template_thresholds.items():
            spin.setParent(None)
        self.template_thresholds.clear()
        
        # Get all available templates organized by category
        categories = ["decorations", "main", "market", "offer", "advert"]
        
        # Create horizontal layout for all categories
        categories_row = QHBoxLayout()
        categories_row.setSpacing(20)  # Reduced space between categories
        
        for category in categories:
            # Get templates for this category
            templates = self.bot_core.template_detector.get_available_templates(category)
            
            if not templates:
                continue
            
            # Create category group box - compact
            category_group = QGroupBox(category.title())
            category_layout = QVBoxLayout()
            category_layout.setSpacing(8)
            category_layout.setContentsMargins(12, 12, 12, 12)
            
            for template_name in templates:
                # Template row - compact
                template_row = QHBoxLayout()
                template_row.setSpacing(15)  # More space between text and value
                
                # Template name label - shortened
                template_display_name = template_name.split('/')[-1] if '/' in template_name else template_name
                # Truncate long names
                if len(template_display_name) > 15:
                    template_display_name = template_display_name[:12] + "..."
                label = QLabel(f"{template_display_name}:")
                label.setMinimumWidth(120)
                label.setMaximumWidth(120)
                template_row.addWidget(label)
                
                # Threshold spinbox - uniform width
                spin = QDoubleSpinBox()
                spin.setRange(0.1, 1.0)
                spin.setSingleStep(0.05)
                spin.setValue(0.0)  # No default - must be configured explicitly
                spin.setDecimals(2)
                spin.setEnabled(False)  # Disabled until loaded from config
                spin.setToolTip(f"Detection threshold for {template_name}")
                spin.setMinimumWidth(80)  # Same as other inputs
                spin.setMaximumWidth(80)  # Same as other inputs
                
                self.template_thresholds[template_name] = spin
                template_row.addWidget(spin)
                
                category_layout.addLayout(template_row)
            
            category_group.setLayout(category_layout)
            category_group.setMaximumWidth(210)  # Slightly narrower
            categories_row.addWidget(category_group)
        
        # Add stretch to push everything to the left
        categories_row.addStretch()
        
        parent_layout.addLayout(categories_row)
    

    
    def _calculate_polygon_area(self, polygon):
        """Calculate polygon area using shoelace formula"""
        if len(polygon) < 3:
            return 0
        
        area = 0
        n = len(polygon)
        for i in range(n):
            j = (i + 1) % n
            area += polygon[i][0] * polygon[j][1]
            area -= polygon[j][0] * polygon[i][1]
        return abs(area) / 2.0 