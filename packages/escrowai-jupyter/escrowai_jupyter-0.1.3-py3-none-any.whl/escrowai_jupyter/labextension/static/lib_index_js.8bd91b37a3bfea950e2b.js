"use strict";
(self["webpackChunkescrowai_jupyter"] = self["webpackChunkescrowai_jupyter"] || []).push([["lib_index_js"],{

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
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var ansi_up__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ansi_up */ "webpack/sharing/consume/default/ansi_up/ansi_up");
/* harmony import */ var ansi_up__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(ansi_up__WEBPACK_IMPORTED_MODULE_2__);




const ansi_up = new ansi_up__WEBPACK_IMPORTED_MODULE_2__.AnsiUp();
class ProgressWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    constructor() {
        super();
        this.addClass('jp-EscrowAI-progress');
        // Create the progress container
        const container = document.createElement('div');
        container.className = 'escrowai-progress-container';
        // Create progress elements
        this.stepLabel = document.createElement('div');
        this.stepLabel.className = 'escrowai-step-label';
        this.progressBar = document.createElement('div');
        this.progressBar.className = 'escrowai-progress-bar';
        this.progressFill = document.createElement('div');
        this.progressFill.className = 'escrowai-progress-fill';
        this.progressBar.appendChild(this.progressFill);
        // Create a fixed header that contains the step label and progress bar
        const headerContainer = document.createElement('div');
        headerContainer.className = 'escrowai-header-container';
        headerContainer.appendChild(this.stepLabel);
        headerContainer.appendChild(this.progressBar);
        this.detailsLabel = document.createElement('div');
        this.detailsLabel.className = 'escrowai-details-label';
        // Add elements to container
        container.appendChild(headerContainer);
        container.appendChild(this.detailsLabel);
        this.node.appendChild(container);
        // Initialize state
        this.currentStep = 'Initializing...';
        this.latestByStep = new Map();
        // Initialize with starting state
        this.updateProgress(this.currentStep, 'Preparing to start upload...', 0);
        console.log('ProgressWidget: Initialization complete');
    }
    setErrorState(isError) {
        if (isError) {
            this.stepLabel.classList.add('error');
            this.progressFill.classList.add('error');
        }
        else {
            this.stepLabel.classList.remove('error');
            this.progressFill.classList.remove('error');
        }
    }
    scrollToBottom() {
        // Ensure scrolling to the bottom
        this.detailsLabel.scrollTop = this.detailsLabel.scrollHeight;
    }
    updateProgress(step, details, progress) {
        console.log('updateProgress:', { step, details, progress });
        // Check if this is an error state
        const isError = step === 'Error';
        this.setErrorState(isError);
        // Update step if it has changed
        if (step !== this.currentStep) {
            console.log('Step changed from', this.currentStep, 'to', step);
            this.currentStep = step;
            this.stepLabel.textContent = step;
        }
        // Add new details if it's not empty
        if (details && details.trim()) {
            // Store only the latest update for this step
            const timestamp = new Date().toLocaleTimeString();
            this.latestByStep.set(step, `[${timestamp}] ${details}`);
            // Update the display
            this.updateDisplay();
        }
        // Update progress bar
        const progressWidth = `${Math.min(100, Math.max(0, progress))}%`;
        this.progressFill.style.width = progressWidth;
        // Scroll to bottom
        this.scrollToBottom();
    }
    updateDisplay() {
        // Only show the current step's output
        if (this.latestByStep.has(this.currentStep)) {
            const content = this.latestByStep.get(this.currentStep);
            const stepContent = `<div class="escrowai-output-line">${ansi_up.ansi_to_html(content)}</div>`;
            this.detailsLabel.innerHTML = stepContent;
        }
        else {
            this.detailsLabel.innerHTML = '';
        }
    }
}
/**
 * Initialization data for the escrowai-jupyter extension.
 */
const plugin = {
    id: 'escrowai-jupyter:plugin',
    description: 'An extension to encrypt and upload the working directory to EscrowAI',
    autoStart: true,
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette],
    activate: (app, palette) => {
        console.log('EscrowAI Extension: Activating...');
        const command = 'escrowai-jupyter:run-script';
        app.commands.addCommand(command, {
            label: 'Upload to EscrowAI',
            execute: async () => {
                console.log('EscrowAI Extension: Command executed');
                // Create and show the progress widget
                const content = new ProgressWidget();
                const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({ content });
                widget.id = 'escrowai-progress';
                widget.title.label = 'EscrowAI Upload Progress';
                widget.title.closable = true;
                // Add the widget to the main area
                app.shell.add(widget, 'main');
                widget.update();
                try {
                    console.log('EscrowAI Extension: Starting EventSource connection...');
                    const eventSource = new EventSource('/escrowai_jupyter/run-script');
                    eventSource.onopen = () => {
                        console.log('EscrowAI Extension: EventSource connection opened');
                    };
                    eventSource.onmessage = (event) => {
                        console.log('EscrowAI Extension: Received event data:', event.data);
                        const data = JSON.parse(event.data);
                        console.log('EscrowAI Extension: Parsed event data:', data);
                        if (data.status === 'running') {
                            console.log('EscrowAI Extension: Processing running status update');
                            content.updateProgress(data.step || 'Processing...', data.details || '', data.progress || 0);
                        }
                        else if (data.status === 'complete') {
                            console.log('EscrowAI Extension: Processing completion');
                            eventSource.close();
                            content.updateProgress('Complete', 'Upload successful!', 100);
                            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                                title: 'Upload Complete',
                                body: new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget({ node: Private.createHTMLNode('Successfully uploaded to EscrowAI!') }),
                                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()]
                            });
                        }
                        else if (data.status === 'error') {
                            console.error('EscrowAI Extension: Processing error:', data.error);
                            eventSource.close();
                            const errorMessage = data.error || 'Upload failed';
                            content.updateProgress('Error', errorMessage, 0);
                            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                                title: 'Upload Failed',
                                body: new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget({ node: Private.createHTMLNode(`Error: ${ansi_up.ansi_to_html(errorMessage)}`) }),
                                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()]
                            });
                        }
                    };
                    eventSource.onerror = (error) => {
                        console.error('EscrowAI Extension: EventSource error:', error);
                        eventSource.close();
                        const errorMessage = 'Connection failed';
                        content.updateProgress('Error', errorMessage, 0);
                        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                            title: 'Upload Failed',
                            body: new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget({ node: Private.createHTMLNode(`Error: ${errorMessage}`) }),
                            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()]
                        });
                    };
                }
                catch (error) {
                    const errorMessage = String(error);
                    content.updateProgress('Error', errorMessage, 0);
                    (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                        title: 'Upload Failed',
                        body: new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget({ node: Private.createHTMLNode(`Error: ${ansi_up.ansi_to_html(errorMessage)}`) }),
                        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()]
                    });
                }
            }
        });
        if (palette) {
            palette.addItem({ command, category: 'Extensions' });
        }
        console.log('EscrowAI Extension: Activation complete');
    }
};
/**
 * Private utility functions
 */
var Private;
(function (Private) {
    function createHTMLNode(html) {
        const node = document.createElement('div');
        node.innerHTML = html;
        return node;
    }
    Private.createHTMLNode = createHTMLNode;
})(Private || (Private = {}));
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.8bd91b37a3bfea950e2b.js.map