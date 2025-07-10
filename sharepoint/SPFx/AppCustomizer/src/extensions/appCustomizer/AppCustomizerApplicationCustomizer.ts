import { Log } from '@microsoft/sp-core-library';
import {
  BaseApplicationCustomizer
} from '@microsoft/sp-application-base';

import * as strings from 'AppCustomizerApplicationCustomizerStrings';

const LOG_SOURCE: string = 'AppCustomizerApplicationCustomizer';

/**
 * If your command set uses the ClientSideComponentProperties JSON input,
 * it will be deserialized into the BaseExtension.properties object.
 * You can define an interface to describe it.
 */
export interface IAppCustomizerApplicationCustomizerProperties {
  // This is an example; replace with your own property
  testMessage: string;
}

/** A Custom Action which can be run during execution of a Client Side Application */
export default class AppCustomizerApplicationCustomizer
  extends BaseApplicationCustomizer<IAppCustomizerApplicationCustomizerProperties> {

  public onInit(): Promise<void> {
    Log.info(LOG_SOURCE, `Initialized ${strings.Title}`);
    const head = document.getElementsByTagName("head")[0];
    const style = document.createElement("link");
    style.rel = "stylesheet";
    style.href = `/sites/${YourSite}/SiteAssets/index.css`;
    head.appendChild(style);

    return Promise.resolve();
  }
}
