/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package org.micromanager.multichannelshading;

import mmcorej.CMMCore;
import org.micromanager.api.ScriptInterface;

/**
 *
 * @author kthorn
 */
public class MultiChannelShading implements org.micromanager.api.MMPlugin {
   public static final String menuName = "Multi-Channel Shading";
   public static final String tooltipDescription =
      "Apply dark subtraction and flat-field correction";

   public static String versionNumber = "0.1";
   private ScriptInterface gui_;
   private MultiChannelShadingForm myFrame_;
   
    @Override
    public void dispose() {
    }

    @Override
    public void setApp(ScriptInterface si) {
      gui_ = si;                                        
      if (myFrame_ == null)
         myFrame_ = new MultiChannelShadingForm(gui_);
      myFrame_.setVisible(true);
      
      // Used to change the background layout of the form.  Does not work on Windows
      gui_.addMMBackgroundListener(myFrame_);    
    }

    @Override
    public void show() {
    }

    @Override
    public String getDescription() {
        return tooltipDescription;
    }

    @Override
    public String getInfo() {
        return tooltipDescription;
    }

    @Override
    public String getVersion() {
        return versionNumber;
    }

    @Override
    public String getCopyright() {
       return "University of California, 2014";
    }
    
}
