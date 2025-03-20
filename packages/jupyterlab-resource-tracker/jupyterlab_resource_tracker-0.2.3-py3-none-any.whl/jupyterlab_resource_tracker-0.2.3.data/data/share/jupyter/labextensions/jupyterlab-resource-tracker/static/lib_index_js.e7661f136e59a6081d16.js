"use strict";
(self["webpackChunkjupyterlab_resource_tracker"] = self["webpackChunkjupyterlab_resource_tracker"] || []).push([["lib_index_js"],{

/***/ "./lib/components/DashboardComponent.js":
/*!**********************************************!*\
  !*** ./lib/components/DashboardComponent.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mui_material_Box__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material/Box */ "./node_modules/@mui/material/Box/Box.js");
/* harmony import */ var _SummaryComponent__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./SummaryComponent */ "./lib/components/SummaryComponent.js");
/* harmony import */ var _DetailsComponent__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./DetailsComponent */ "./lib/components/DetailsComponent.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../handler */ "./lib/handler.js");






// import LogsComponent from './LogsComponent';
const DashboardComponent = (props) => {
    const [summaryList, setSummaryList] = react__WEBPACK_IMPORTED_MODULE_0___default().useState([]);
    const [detailList, setDetailList] = react__WEBPACK_IMPORTED_MODULE_0___default().useState([]);
    react__WEBPACK_IMPORTED_MODULE_0___default().useEffect(() => {
        getLogs();
    }, []);
    const getLogs = async () => {
        try {
            const response = await (0,_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)('usages-costs/logs', {
                method: "GET",
            }).then(data => {
                console.log(data);
                return data;
            }).catch(reason => {
                console.error(`The jupyterlab_resource_tracker server extension appears to be missing.\n${reason}`);
            });
            if (response) {
                setSummaryList(response.summary);
                setDetailList(response.details);
            }
        }
        catch (error) {
            console.log(`Error => ${JSON.stringify(error, null, 2)}`);
        }
    };
    const handleClickOpen = () => {
        getLogs();
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: { height: '100%', overflowY: 'auto' } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Button, { onClick: handleClickOpen }, "REFRESH"),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_SummaryComponent__WEBPACK_IMPORTED_MODULE_4__["default"], { summary: summaryList }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Divider, null),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_DetailsComponent__WEBPACK_IMPORTED_MODULE_5__["default"], { details: detailList }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Divider, null))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (DashboardComponent);
react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.CssBaseline, null);


/***/ }),

/***/ "./lib/components/DetailsComponent.js":
/*!********************************************!*\
  !*** ./lib/components/DetailsComponent.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mui_x_data_grid__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/x-data-grid */ "webpack/sharing/consume/default/@mui/x-data-grid/@mui/x-data-grid");
/* harmony import */ var _mui_x_data_grid__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_mui_x_data_grid__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _mui_material_Typography__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material/Typography */ "./node_modules/@mui/material/Typography/Typography.js");
/* harmony import */ var _mui_material_Paper__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/material/Paper */ "./node_modules/@mui/material/Paper/Paper.js");





const DetailsComponent = (props) => {
    const columns2 = [
        { field: 'id', headerName: 'ID', width: 50 },
        { field: 'username', headerName: 'User', width: 70 },
        { field: 'ec2StandardTime', headerName: 'Standard (time)', width: 110 },
        { field: 'ec2StandardCost', headerName: 'Standard ($)', type: 'number', width: 110 },
        { field: 'ec2LargeTime', headerName: 'Large (time)', width: 110 },
        { field: 'ec2LargeCost', headerName: 'Large ($)', type: 'number', width: 110 },
        { field: 'ec2ExtraTime', headerName: 'Extra (time)', width: 110 },
        { field: 'ec2ExtraCost', headerName: 'Extra ($)', type: 'number', width: 110 },
        { field: 'ec22xLargeTime', headerName: '2x Large (time)', width: 130 },
        { field: 'ec22xLargeCost', headerName: '2x Large ($)', type: 'number', width: 110 },
        { field: 'ec28xLargeTime', headerName: '8x Large (time)', width: 130 },
        { field: 'ec28xLargeCost', headerName: '8x Large ($)', type: 'number', width: 110 },
        { field: 'gpuNodeTime', headerName: 'GPU Node (time)', width: 130 },
    ];
    const paginationModel = { page: 0, pageSize: 5 };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_3__["default"], { variant: "h6", gutterBottom: true }, "Intances type per User"),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Paper__WEBPACK_IMPORTED_MODULE_4__["default"], { sx: { height: 400, width: '100%', mb: 2 } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_x_data_grid__WEBPACK_IMPORTED_MODULE_2__.DataGrid, { rows: props.details, columns: columns2, initialState: { pagination: { paginationModel } }, pageSizeOptions: [5, 10], checkboxSelection: true, sx: { border: 0 } }))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (DetailsComponent);
react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.CssBaseline, null);


/***/ }),

/***/ "./lib/components/SummaryComponent.js":
/*!********************************************!*\
  !*** ./lib/components/SummaryComponent.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mui_x_data_grid__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/x-data-grid */ "webpack/sharing/consume/default/@mui/x-data-grid/@mui/x-data-grid");
/* harmony import */ var _mui_x_data_grid__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_mui_x_data_grid__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _mui_material_Typography__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material/Typography */ "./node_modules/@mui/material/Typography/Typography.js");
/* harmony import */ var _mui_material_Paper__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/material/Paper */ "./node_modules/@mui/material/Paper/Paper.js");





const SummaryComponent = (props) => {
    const columns = [
        { field: 'id', headerName: 'ID', width: 70 },
        { field: 'username', headerName: 'User', width: 130 },
        { field: 'nbTime', headerName: 'Notebook time', width: 130 },
        { field: 'cost', headerName: 'ToDate Cost ($)', type: 'number', width: 130, },
    ];
    const paginationModel = { page: 0, pageSize: 5 };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_3__["default"], { variant: "h6", gutterBottom: true }, "Costs per User"),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Paper__WEBPACK_IMPORTED_MODULE_4__["default"], { sx: { height: 400, width: '100%', mb: 2 } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_x_data_grid__WEBPACK_IMPORTED_MODULE_2__.DataGrid, { rows: props.summary, columns: columns, initialState: { pagination: { paginationModel } }, pageSizeOptions: [5, 10], checkboxSelection: true, sx: { border: 0 } }))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (SummaryComponent);
react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.CssBaseline, null);


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   requestAPI: () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab-resource-tracker', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _widgets_DashboardWidget__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./widgets/DashboardWidget */ "./lib/widgets/DashboardWidget.js");






const PLUGIN_ID = 'jupyterlab-resource-tracker:plugin';
const PALETTE_CATEGORY = 'Admin tools';
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.createNew = 'jupyterlab-resource-tracker:open-dashboard';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the jupyterlab-resource-tracker extension.
 */
const plugin = {
    id: PLUGIN_ID,
    description: 'A JupyterLab extension.',
    autoStart: true,
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry, _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__.ILauncher, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette],
    activate: (app, settingRegistry, launcher, palette) => {
        console.log('JupyterLab extension jupyterlab-resource-tracker is activated!');
        if (settingRegistry) {
            settingRegistry
                .load(plugin.id)
                .then(settings => {
                console.log('jupyterlab-resource-tracker settings loaded:', settings.composite);
            })
                .catch(reason => {
                console.error('Failed to load settings for jupyterlab-resource-tracker.', reason);
            });
        }
        (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('get-example')
            .then(data => {
            console.log(data);
        })
            .catch(reason => {
            console.error(`The jupyterlab_resource_tracker server extension appears to be missing.\n${reason}`);
        });
        const { commands } = app;
        const command = CommandIDs.createNew;
        // const sideBarContent = new NBQueueSideBarWidget(s3BucketId);
        // const sideBarWidget = new MainAreaWidget<NBQueueSideBarWidget>({
        //   content: sideBarContent
        // });
        // sideBarWidget.toolbar.hide();
        // sideBarWidget.title.icon = runIcon;
        // sideBarWidget.title.caption = 'NBQueue job list';
        // app.shell.add(sideBarWidget, 'right', { rank: 501 });
        // Define a widget creator function,
        // then call it to make a new widget
        const newWidget = () => {
            // Create a blank content widget inside of a MainAreaWidget
            const dashboardContent = new _widgets_DashboardWidget__WEBPACK_IMPORTED_MODULE_5__.DashboardWidget();
            const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({
                content: dashboardContent
            });
            widget.id = 'resource-tracker-dashboard';
            widget.title.label = 'Resource Tracker';
            widget.title.closable = true;
            return widget;
        };
        let widget = newWidget();
        commands.addCommand(command, {
            label: 'Resource Tracker',
            caption: 'Resource Tracker',
            icon: args => (args['isPalette'] ? undefined : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.inspectorIcon),
            execute: async (args) => {
                console.log('Command executed');
                // Regenerate the widget if disposed
                if (widget.isDisposed) {
                    widget = newWidget();
                }
                if (!widget.isAttached) {
                    // Attach the widget to the main work area if it's not there
                    app.shell.add(widget, 'main');
                }
                // Activate the widget
                app.shell.activateById(widget.id);
            }
        });
        if (launcher) {
            launcher.add({
                command,
                category: 'Admin tools',
                rank: 1
            });
        }
        if (palette) {
            palette.addItem({
                command,
                args: { isPalette: true },
                category: PALETTE_CATEGORY
            });
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/widgets/DashboardWidget.js":
/*!****************************************!*\
  !*** ./lib/widgets/DashboardWidget.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DashboardWidget: () => (/* binding */ DashboardWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_DashboardComponent__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../components/DashboardComponent */ "./lib/components/DashboardComponent.js");



class DashboardWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor() {
        super();
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_DashboardComponent__WEBPACK_IMPORTED_MODULE_2__["default"], null));
    }
}


/***/ }),

/***/ "./node_modules/@mui/material/Box/Box.js":
/*!***********************************************!*\
  !*** ./node_modules/@mui/material/Box/Box.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _mui_system__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/system */ "./node_modules/@mui/system/esm/createBox/createBox.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _className_index_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../className/index.js */ "./node_modules/@mui/utils/esm/ClassNameGenerator/ClassNameGenerator.js");
/* harmony import */ var _styles_index_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../styles/index.js */ "./node_modules/@mui/material/styles/createTheme.js");
/* harmony import */ var _styles_identifier_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../styles/identifier.js */ "./node_modules/@mui/material/styles/identifier.js");
/* harmony import */ var _boxClasses_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./boxClasses.js */ "./node_modules/@mui/material/Box/boxClasses.js");
'use client';







const defaultTheme = (0,_styles_index_js__WEBPACK_IMPORTED_MODULE_0__["default"])();
const Box = (0,_mui_system__WEBPACK_IMPORTED_MODULE_1__["default"])({
  themeId: _styles_identifier_js__WEBPACK_IMPORTED_MODULE_2__["default"],
  defaultTheme,
  defaultClassName: _boxClasses_js__WEBPACK_IMPORTED_MODULE_3__["default"].root,
  generateClassName: _className_index_js__WEBPACK_IMPORTED_MODULE_4__["default"].generate
});
 true ? Box.propTypes /* remove-proptypes */ = {
  // ┌────────────────────────────── Warning ──────────────────────────────┐
  // │ These PropTypes are generated from the TypeScript type definitions. │
  // │    To update them, edit the d.ts file and run `pnpm proptypes`.     │
  // └─────────────────────────────────────────────────────────────────────┘
  /**
   * @ignore
   */
  children: (prop_types__WEBPACK_IMPORTED_MODULE_5___default().node),
  /**
   * The component used for the root node.
   * Either a string to use a HTML element or a component.
   */
  component: (prop_types__WEBPACK_IMPORTED_MODULE_5___default().elementType),
  /**
   * The system prop that allows defining system overrides as well as additional CSS styles.
   */
  sx: prop_types__WEBPACK_IMPORTED_MODULE_5___default().oneOfType([prop_types__WEBPACK_IMPORTED_MODULE_5___default().arrayOf(prop_types__WEBPACK_IMPORTED_MODULE_5___default().oneOfType([(prop_types__WEBPACK_IMPORTED_MODULE_5___default().func), (prop_types__WEBPACK_IMPORTED_MODULE_5___default().object), (prop_types__WEBPACK_IMPORTED_MODULE_5___default().bool)])), (prop_types__WEBPACK_IMPORTED_MODULE_5___default().func), (prop_types__WEBPACK_IMPORTED_MODULE_5___default().object)])
} : 0;
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Box);

/***/ }),

/***/ "./node_modules/@mui/material/Box/boxClasses.js":
/*!******************************************************!*\
  !*** ./node_modules/@mui/material/Box/boxClasses.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _mui_utils_generateUtilityClasses__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @mui/utils/generateUtilityClasses */ "./node_modules/@mui/utils/esm/generateUtilityClasses/generateUtilityClasses.js");

const boxClasses = (0,_mui_utils_generateUtilityClasses__WEBPACK_IMPORTED_MODULE_0__["default"])('MuiBox', ['root']);
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (boxClasses);

/***/ }),

/***/ "./node_modules/@mui/system/esm/createBox/createBox.js":
/*!*************************************************************!*\
  !*** ./node_modules/@mui/system/esm/createBox/createBox.js ***!
  \*************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ createBox)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var clsx__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! clsx */ "./node_modules/clsx/dist/clsx.mjs");
/* harmony import */ var _mui_styled_engine__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/styled-engine */ "./node_modules/@mui/styled-engine/index.js");
/* harmony import */ var _styleFunctionSx_index_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../styleFunctionSx/index.js */ "./node_modules/@mui/system/esm/styleFunctionSx/styleFunctionSx.js");
/* harmony import */ var _styleFunctionSx_index_js__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../styleFunctionSx/index.js */ "./node_modules/@mui/system/esm/styleFunctionSx/extendSxProp.js");
/* harmony import */ var _useTheme_index_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../useTheme/index.js */ "./node_modules/@mui/system/esm/useTheme/useTheme.js");
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
'use client';







function createBox(options = {}) {
  const {
    themeId,
    defaultTheme,
    defaultClassName = 'MuiBox-root',
    generateClassName
  } = options;
  const BoxRoot = (0,_mui_styled_engine__WEBPACK_IMPORTED_MODULE_3__["default"])('div', {
    shouldForwardProp: prop => prop !== 'theme' && prop !== 'sx' && prop !== 'as'
  })(_styleFunctionSx_index_js__WEBPACK_IMPORTED_MODULE_4__["default"]);
  const Box = /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.forwardRef(function Box(inProps, ref) {
    const theme = (0,_useTheme_index_js__WEBPACK_IMPORTED_MODULE_5__["default"])(defaultTheme);
    const {
      className,
      component = 'div',
      ...other
    } = (0,_styleFunctionSx_index_js__WEBPACK_IMPORTED_MODULE_6__["default"])(inProps);
    return /*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_2__.jsx)(BoxRoot, {
      as: component,
      ref: ref,
      className: (0,clsx__WEBPACK_IMPORTED_MODULE_1__["default"])(className, generateClassName ? generateClassName(defaultClassName) : defaultClassName),
      theme: themeId ? theme[themeId] || theme : theme,
      ...other
    });
  });
  return Box;
}

/***/ })

}]);
//# sourceMappingURL=lib_index_js.e7661f136e59a6081d16.js.map