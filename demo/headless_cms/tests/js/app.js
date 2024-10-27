const { Component, loadFile, onWillStart, onMounted, mount, xml, App } = owl;


// -------------------------------------------------------------------------
// Root Component
// -------------------------------------------------------------------------
class Root extends Component {

}

// -------------------------------------------------------------------------
// Setup
// -------------------------------------------------------------------------
async function setup() {
  const templates = await loadFile("template.xml");

  Root.template = xml `${templates}`;
  // mount(Root, document.body);

  const app = new App(Root);
  app.mount(document.body);
}

setup();
