


<!DOCTYPE html>
<html>
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# githubog: http://ogp.me/ns/fb/githubog#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=10">
        <title>thrift/lib/js/src/thrift.js at master · apache/thrift</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub" />
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub" />
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-114.png" />
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114.png" />
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-144.png" />
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144.png" />
    <link rel="logo" type="image/svg" href="https://github-media-downloads.s3.amazonaws.com/github-logo.svg" />
    <meta property="og:image" content="https://github.global.ssl.fastly.net/images/modules/logos_page/Octocat.png">
    <meta name="hostname" content="github-fe117-cp1-prd.iad.github.net">
    <meta name="ruby" content="ruby 1.9.3p194-tcs-github-tcmalloc (0e75de19f8) [x86_64-linux]">
    <link rel="assets" href="https://github.global.ssl.fastly.net/">
    <link rel="conduit-xhr" href="https://ghconduit.com:25035/">
    <link rel="xhr-socket" href="/_sockets" />
    


    <meta name="msapplication-TileImage" content="/windows-tile.png" />
    <meta name="msapplication-TileColor" content="#ffffff" />
    <meta name="selected-link" value="repo_source" data-pjax-transient />
    <meta content="collector.githubapp.com" name="octolytics-host" /><meta content="collector-cdn.github.com" name="octolytics-script-host" /><meta content="github" name="octolytics-app-id" /><meta content="121A0264:678F:87BF2CF:527D2EB8" name="octolytics-dimension-request_id" /><meta content="938567" name="octolytics-actor-id" /><meta content="abhardwaj" name="octolytics-actor-login" /><meta content="387c96112d9d072d7085f1bfb97e74e4b2fd0cd1075b4e7cbe5064c9fd307039" name="octolytics-actor-hash" />
    

    
    
    <link rel="icon" type="image/x-icon" href="/favicon.ico" />

    <meta content="authenticity_token" name="csrf-param" />
<meta content="Bbmw0DUsm3I9TU5LlMHkfRUyUCxwCLRsYxMllL3KH4k=" name="csrf-token" />

    <link href="https://github.global.ssl.fastly.net/assets/github-a8a3849004502491c476c2c9fb91967ce28667f8.css" media="all" rel="stylesheet" type="text/css" />
    <link href="https://github.global.ssl.fastly.net/assets/github2-861981c03b50bcbc64ba20390c7f2c0b61e1c9d5.css" media="all" rel="stylesheet" type="text/css" />
    

    

      <script src="https://github.global.ssl.fastly.net/assets/frameworks-bca527bb59d94c16d6bf2a759779d7953fa41e76.js" type="text/javascript"></script>
      <script src="https://github.global.ssl.fastly.net/assets/github-5b80d04c85d769b66d1817d8cf8e5182eb0ed46c.js" type="text/javascript"></script>
      
      <meta http-equiv="x-pjax-version" content="fd5ab9d01ddadeca2522d439d385f35a">

        <link data-pjax-transient rel='permalink' href='/apache/thrift/blob/f4e6e62ea091b94322ecc99756269dbee1c06380/lib/js/src/thrift.js'>
  <meta property="og:title" content="thrift"/>
  <meta property="og:type" content="githubog:gitrepository"/>
  <meta property="og:url" content="https://github.com/apache/thrift"/>
  <meta property="og:image" content="https://github.global.ssl.fastly.net/images/gravatars/gravatar-user-420.png"/>
  <meta property="og:site_name" content="GitHub"/>
  <meta property="og:description" content="thrift - Mirror of Apache Thrift (incubating)"/>

  <meta name="description" content="thrift - Mirror of Apache Thrift (incubating)" />

  <meta content="47359" name="octolytics-dimension-user_id" /><meta content="apache" name="octolytics-dimension-user_login" /><meta content="310611" name="octolytics-dimension-repository_id" /><meta content="apache/thrift" name="octolytics-dimension-repository_nwo" /><meta content="true" name="octolytics-dimension-repository_public" /><meta content="false" name="octolytics-dimension-repository_is_fork" /><meta content="310611" name="octolytics-dimension-repository_network_root_id" /><meta content="apache/thrift" name="octolytics-dimension-repository_network_root_nwo" />
  <link href="https://github.com/apache/thrift/commits/master.atom" rel="alternate" title="Recent Commits to thrift:master" type="application/atom+xml" />

  </head>


  <body class="logged_in  env-production macintosh vis-public mirror   page-blob">
    <div class="wrapper">
      
      
      
      


      <div class="header header-logged-in true">
  <div class="container clearfix">

    <a class="header-logo-invertocat" href="https://github.com/">
  <span class="mega-octicon octicon-mark-github"></span>
</a>

    
    <a href="/notifications" class="notification-indicator tooltipped downwards" data-gotokey="n" title="You have no unread notifications">
        <span class="mail-status all-read"></span>
</a>

      <div class="command-bar js-command-bar  in-repository">
          <form accept-charset="UTF-8" action="/search" class="command-bar-form" id="top_search_form" method="get">

<input type="text" data-hotkey="/ s" name="q" id="js-command-bar-field" placeholder="Search or type a command" tabindex="1" autocapitalize="off"
    
    data-username="abhardwaj"
      data-repo="apache/thrift"
      data-branch="master"
      data-sha="19eb51150f3e1a084cecc6d64304ebf90b51f3a3"
  >

    <input type="hidden" name="nwo" value="apache/thrift" />

    <div class="select-menu js-menu-container js-select-menu search-context-select-menu">
      <span class="minibutton select-menu-button js-menu-target">
        <span class="js-select-button">This repository</span>
      </span>

      <div class="select-menu-modal-holder js-menu-content js-navigation-container">
        <div class="select-menu-modal">

          <div class="select-menu-item js-navigation-item js-this-repository-navigation-item selected">
            <span class="select-menu-item-icon octicon octicon-check"></span>
            <input type="radio" class="js-search-this-repository" name="search_target" value="repository" checked="checked" />
            <div class="select-menu-item-text js-select-button-text">This repository</div>
          </div> <!-- /.select-menu-item -->

          <div class="select-menu-item js-navigation-item js-all-repositories-navigation-item">
            <span class="select-menu-item-icon octicon octicon-check"></span>
            <input type="radio" name="search_target" value="global" />
            <div class="select-menu-item-text js-select-button-text">All repositories</div>
          </div> <!-- /.select-menu-item -->

        </div>
      </div>
    </div>

  <span class="octicon help tooltipped downwards" title="Show command bar help">
    <span class="octicon octicon-question"></span>
  </span>


  <input type="hidden" name="ref" value="cmdform">

</form>
        <ul class="top-nav">
          <li class="explore"><a href="/explore">Explore</a></li>
            <li><a href="https://gist.github.com">Gist</a></li>
            <li><a href="/blog">Blog</a></li>
          <li><a href="https://help.github.com">Help</a></li>
        </ul>
      </div>

    


  <ul id="user-links">
    <li>
      <a href="/abhardwaj" class="name">
        <img height="20" src="https://1.gravatar.com/avatar/f9670e359d15e36a3bf52bc777269177?d=https%3A%2F%2Fidenticons.github.com%2F0e1e98fcaa122509966d78d0b66720e6.png&amp;r=x&amp;s=140" width="20" /> abhardwaj
      </a>
    </li>

      <li>
        <a href="/new" id="new_repo" class="tooltipped downwards" title="Create a new repo" aria-label="Create a new repo">
          <span class="octicon octicon-repo-create"></span>
        </a>
      </li>

      <li>
        <a href="/settings/profile" id="account_settings"
          class="tooltipped downwards"
          aria-label="Account settings "
          title="Account settings ">
          <span class="octicon octicon-tools"></span>
        </a>
      </li>
      <li>
        <a class="tooltipped downwards" href="/logout" data-method="post" id="logout" title="Sign out" aria-label="Sign out">
          <span class="octicon octicon-log-out"></span>
        </a>
      </li>

  </ul>

<div class="js-new-dropdown-contents hidden">
  

<ul class="dropdown-menu">
  <li>
    <a href="/new"><span class="octicon octicon-repo-create"></span> New repository</a>
  </li>
  <li>
    <a href="/organizations/new"><span class="octicon octicon-organization"></span> New organization</a>
  </li>



</ul>

</div>


    
  </div>
</div>

      

      




          <div class="site" itemscope itemtype="http://schema.org/WebPage">
    
    <div class="pagehead repohead instapaper_ignore readability-menu">
      <div class="container">
        

<ul class="pagehead-actions">

    <li class="subscription">
      <form accept-charset="UTF-8" action="/notifications/subscribe" class="js-social-container" data-autosubmit="true" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="authenticity_token" type="hidden" value="Bbmw0DUsm3I9TU5LlMHkfRUyUCxwCLRsYxMllL3KH4k=" /></div>  <input id="repository_id" name="repository_id" type="hidden" value="310611" />

    <div class="select-menu js-menu-container js-select-menu">
      <a class="social-count js-social-count" href="/apache/thrift/watchers">
        83
      </a>
      <span class="minibutton select-menu-button with-count js-menu-target" role="button" tabindex="0">
        <span class="js-select-button">
          <span class="octicon octicon-eye-watch"></span>
          Watch
        </span>
      </span>

      <div class="select-menu-modal-holder">
        <div class="select-menu-modal subscription-menu-modal js-menu-content">
          <div class="select-menu-header">
            <span class="select-menu-title">Notification status</span>
            <span class="octicon octicon-remove-close js-menu-close"></span>
          </div> <!-- /.select-menu-header -->

          <div class="select-menu-list js-navigation-container" role="menu">

            <div class="select-menu-item js-navigation-item selected" role="menuitem" tabindex="0">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <div class="select-menu-item-text">
                <input checked="checked" id="do_included" name="do" type="radio" value="included" />
                <h4>Not watching</h4>
                <span class="description">You only receive notifications for discussions in which you participate or are @mentioned.</span>
                <span class="js-select-button-text hidden-select-button-text">
                  <span class="octicon octicon-eye-watch"></span>
                  Watch
                </span>
              </div>
            </div> <!-- /.select-menu-item -->

            <div class="select-menu-item js-navigation-item " role="menuitem" tabindex="0">
              <span class="select-menu-item-icon octicon octicon octicon-check"></span>
              <div class="select-menu-item-text">
                <input id="do_subscribed" name="do" type="radio" value="subscribed" />
                <h4>Watching</h4>
                <span class="description">You receive notifications for all discussions in this repository.</span>
                <span class="js-select-button-text hidden-select-button-text">
                  <span class="octicon octicon-eye-unwatch"></span>
                  Unwatch
                </span>
              </div>
            </div> <!-- /.select-menu-item -->

            <div class="select-menu-item js-navigation-item " role="menuitem" tabindex="0">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <div class="select-menu-item-text">
                <input id="do_ignore" name="do" type="radio" value="ignore" />
                <h4>Ignoring</h4>
                <span class="description">You do not receive any notifications for discussions in this repository.</span>
                <span class="js-select-button-text hidden-select-button-text">
                  <span class="octicon octicon-mute"></span>
                  Stop ignoring
                </span>
              </div>
            </div> <!-- /.select-menu-item -->

          </div> <!-- /.select-menu-list -->

        </div> <!-- /.select-menu-modal -->
      </div> <!-- /.select-menu-modal-holder -->
    </div> <!-- /.select-menu -->

</form>
    </li>

  <li>
  

  <div class="js-toggler-container js-social-container starring-container ">
    <a href="/apache/thrift/unstar"
      class="minibutton with-count js-toggler-target star-button starred upwards"
      title="Unstar this repository" data-remote="true" data-method="post" rel="nofollow">
      <span class="octicon octicon-star-delete"></span><span class="text">Unstar</span>
    </a>

    <a href="/apache/thrift/star"
      class="minibutton with-count js-toggler-target star-button unstarred upwards"
      title="Star this repository" data-remote="true" data-method="post" rel="nofollow">
      <span class="octicon octicon-star"></span><span class="text">Star</span>
    </a>

      <a class="social-count js-social-count" href="/apache/thrift/stargazers">
        730
      </a>
  </div>

  </li>


        <li>
          <a href="/apache/thrift/fork" class="minibutton with-count js-toggler-target fork-button lighter upwards" title="Fork this repo" rel="facebox nofollow">
            <span class="octicon octicon-git-branch-create"></span><span class="text">Fork</span>
          </a>
          <a href="/apache/thrift/network" class="social-count">396</a>
        </li>


</ul>

        <h1 itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="entry-title public">
          <span class="repo-label"><span>public</span></span>
          <span class="mega-octicon octicon-mirror-public"></span>
          <span class="author">
            <a href="/apache" class="url fn" itemprop="url" rel="author"><span itemprop="title">apache</span></a>
          </span>
          <span class="repohead-name-divider">/</span>
          <strong><a href="/apache/thrift" class="js-current-repository js-repo-home-link">thrift</a></strong>

          <span class="page-context-loader">
            <img alt="Octocat-spinner-32" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
          </span>

            <span class="mirror-flag">
              <span class="text">mirrored from <a href="git://git.apache.org/thrift.git">git://git.apache.org/thrift.git</a></span>
            </span>
        </h1>
      </div><!-- /.container -->
    </div><!-- /.repohead -->

    <div class="container">

      <div class="repository-with-sidebar repo-container ">

        <div class="repository-sidebar">
            

<div class="sunken-menu vertical-right repo-nav js-repo-nav js-repository-container-pjax js-octicon-loaders">
  <div class="sunken-menu-contents">
    <ul class="sunken-menu-group">
      <li class="tooltipped leftwards" title="Code">
        <a href="/apache/thrift" aria-label="Code" class="selected js-selected-navigation-item sunken-menu-item" data-gotokey="c" data-pjax="true" data-selected-links="repo_source repo_downloads repo_commits repo_tags repo_branches /apache/thrift">
          <span class="octicon octicon-code"></span> <span class="full-word">Code</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>


      <li class="tooltipped leftwards" title="Pull Requests"><a href="/apache/thrift/pulls" aria-label="Pull Requests" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-gotokey="p" data-selected-links="repo_pulls /apache/thrift/pulls">
            <span class="octicon octicon-git-pull-request"></span> <span class="full-word">Pull Requests</span>
            <span class='counter'>22</span>
            <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>


    </ul>
    <div class="sunken-menu-separator"></div>
    <ul class="sunken-menu-group">

      <li class="tooltipped leftwards" title="Pulse">
        <a href="/apache/thrift/pulse" aria-label="Pulse" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="pulse /apache/thrift/pulse">
          <span class="octicon octicon-pulse"></span> <span class="full-word">Pulse</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

      <li class="tooltipped leftwards" title="Graphs">
        <a href="/apache/thrift/graphs" aria-label="Graphs" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="repo_graphs repo_contributors /apache/thrift/graphs">
          <span class="octicon octicon-graph"></span> <span class="full-word">Graphs</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

      <li class="tooltipped leftwards" title="Network">
        <a href="/apache/thrift/network" aria-label="Network" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-selected-links="repo_network /apache/thrift/network">
          <span class="octicon octicon-git-branch"></span> <span class="full-word">Network</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>
    </ul>


  </div>
</div>

            <div class="only-with-full-nav">
              

  

<div class="clone-url open"
  data-protocol-type="http"
  data-url="/users/set_protocol?protocol_selector=http&amp;protocol_type=clone">
  <h3><strong>HTTPS</strong> clone URL</h3>
  <div class="clone-url-box">
    <input type="text" class="clone js-url-field"
           value="https://github.com/apache/thrift.git" readonly="readonly">

    <span class="js-zeroclipboard url-box-clippy minibutton zeroclipboard-button" data-clipboard-text="https://github.com/apache/thrift.git" data-copied-hint="copied!" title="copy to clipboard"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>

  

<div class="clone-url "
  data-protocol-type="ssh"
  data-url="/users/set_protocol?protocol_selector=ssh&amp;protocol_type=clone">
  <h3><strong>SSH</strong> clone URL</h3>
  <div class="clone-url-box">
    <input type="text" class="clone js-url-field"
           value="git@github.com:apache/thrift.git" readonly="readonly">

    <span class="js-zeroclipboard url-box-clippy minibutton zeroclipboard-button" data-clipboard-text="git@github.com:apache/thrift.git" data-copied-hint="copied!" title="copy to clipboard"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>

  

<div class="clone-url "
  data-protocol-type="subversion"
  data-url="/users/set_protocol?protocol_selector=subversion&amp;protocol_type=clone">
  <h3><strong>Subversion</strong> checkout URL</h3>
  <div class="clone-url-box">
    <input type="text" class="clone js-url-field"
           value="https://github.com/apache/thrift" readonly="readonly">

    <span class="js-zeroclipboard url-box-clippy minibutton zeroclipboard-button" data-clipboard-text="https://github.com/apache/thrift" data-copied-hint="copied!" title="copy to clipboard"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>


<p class="clone-options">You can clone with
      <a href="#" class="js-clone-selector" data-protocol="http">HTTPS</a>,
      <a href="#" class="js-clone-selector" data-protocol="ssh">SSH</a>,
      or <a href="#" class="js-clone-selector" data-protocol="subversion">Subversion</a>.
  <span class="octicon help tooltipped upwards" title="Get help on which URL is right for you.">
    <a href="https://help.github.com/articles/which-remote-url-should-i-use">
    <span class="octicon octicon-question"></span>
    </a>
  </span>
</p>

  <a href="github-mac://openRepo/https://github.com/apache/thrift" data-url="github-mac://openRepo/https://github.com/apache/thrift" class="minibutton sidebar-button js-conduit-rewrite-url">
    <span class="octicon octicon-device-desktop"></span>
    Clone in Desktop
  </a>


              <a href="/apache/thrift/archive/master.zip"
                 class="minibutton sidebar-button"
                 title="Download this repository as a zip file"
                 rel="nofollow">
                <span class="octicon octicon-cloud-download"></span>
                Download ZIP
              </a>
            </div>
        </div><!-- /.repository-sidebar -->

        <div id="js-repo-pjax-container" class="repository-content context-loader-container" data-pjax-container>
          


<!-- blob contrib key: blob_contributors:v21:75efc5a9c4b94aaa8e0f8a38dca968d9 -->

<p title="This is a placeholder element" class="js-history-link-replace hidden"></p>

<a href="/apache/thrift/find/master" data-pjax data-hotkey="t" class="js-show-file-finder" style="display:none">Show File Finder</a>

<div class="file-navigation">
  
  

<div class="select-menu js-menu-container js-select-menu" >
  <span class="minibutton select-menu-button js-menu-target" data-hotkey="w"
    data-master-branch="master"
    data-ref="master"
    role="button" aria-label="Switch branches or tags" tabindex="0">
    <span class="octicon octicon-git-branch"></span>
    <i>branch:</i>
    <span class="js-select-button">master</span>
  </span>

  <div class="select-menu-modal-holder js-menu-content js-navigation-container" data-pjax>

    <div class="select-menu-modal">
      <div class="select-menu-header">
        <span class="select-menu-title">Switch branches/tags</span>
        <span class="octicon octicon-remove-close js-menu-close"></span>
      </div> <!-- /.select-menu-header -->

      <div class="select-menu-filters">
        <div class="select-menu-text-filter">
          <input type="text" aria-label="Filter branches/tags" id="context-commitish-filter-field" class="js-filterable-field js-navigation-enable" placeholder="Filter branches/tags">
        </div>
        <div class="select-menu-tabs">
          <ul>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="branches" class="js-select-menu-tab">Branches</a>
            </li>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="tags" class="js-select-menu-tab">Tags</a>
            </li>
          </ul>
        </div><!-- /.select-menu-tabs -->
      </div><!-- /.select-menu-filters -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="branches">

        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/blob/0.1.x/lib/js/src/thrift.js"
                 data-name="0.1.x"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="0.1.x">0.1.x</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/blob/0.2.x/lib/js/src/thrift.js"
                 data-name="0.2.x"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="0.2.x">0.2.x</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/blob/0.3.x/lib/js/src/thrift.js"
                 data-name="0.3.x"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="0.3.x">0.3.x</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/blob/0.4.x/lib/js/src/thrift.js"
                 data-name="0.4.x"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="0.4.x">0.4.x</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/blob/0.5.x/lib/js/src/thrift.js"
                 data-name="0.5.x"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="0.5.x">0.5.x</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/blob/0.6.x/lib/js/src/thrift.js"
                 data-name="0.6.x"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="0.6.x">0.6.x</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/blob/0.7.x/lib/js/src/thrift.js"
                 data-name="0.7.x"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="0.7.x">0.7.x</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/blob/0.8.x/lib/js/src/thrift.js"
                 data-name="0.8.x"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="0.8.x">0.8.x</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/blob/0.9.1/lib/js/src/thrift.js"
                 data-name="0.9.1"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="0.9.1">0.9.1</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/blob/0.9.x/lib/js/src/thrift.js"
                 data-name="0.9.x"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="0.9.x">0.9.x</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item selected">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/blob/master/lib/js/src/thrift.js"
                 data-name="master"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="master">master</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/blob/py-compiler/lib/js/src/thrift.js"
                 data-name="py-compiler"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="py-compiler">py-compiler</a>
            </div> <!-- /.select-menu-item -->
        </div>

          <div class="select-menu-no-results">Nothing to show</div>
      </div> <!-- /.select-menu-list -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="tags">
        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/tree/thrift-0.9.0/lib/js/src/thrift.js"
                 data-name="thrift-0.9.0"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="thrift-0.9.0">thrift-0.9.0</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/tree/thrift-0.8.0/lib/js/src/thrift.js"
                 data-name="thrift-0.8.0"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="thrift-0.8.0">thrift-0.8.0</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/tree/thrift-0.7.0/lib/js/src/thrift.js"
                 data-name="thrift-0.7.0"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="thrift-0.7.0">thrift-0.7.0</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/tree/thrift-0.6.1/lib/js/src/thrift.js"
                 data-name="thrift-0.6.1"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="thrift-0.6.1">thrift-0.6.1</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/tree/thrift-0.6.0/lib/js/src/thrift.js"
                 data-name="thrift-0.6.0"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="thrift-0.6.0">thrift-0.6.0</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/tree/thrift-0.5.0/lib/js/src/thrift.js"
                 data-name="thrift-0.5.0"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="thrift-0.5.0">thrift-0.5.0</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/tree/thrift-0.4.0/lib/js/src/thrift.js"
                 data-name="thrift-0.4.0"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="thrift-0.4.0">thrift-0.4.0</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/tree/thrift-0.3.0/lib/js/src/thrift.js"
                 data-name="thrift-0.3.0"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="thrift-0.3.0">thrift-0.3.0</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/tree/thrift-0.2.0/lib/js/src/thrift.js"
                 data-name="thrift-0.2.0"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="thrift-0.2.0">thrift-0.2.0</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/apache/thrift/tree/0.5.0/lib/js/src/thrift.js"
                 data-name="0.5.0"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="0.5.0">0.5.0</a>
            </div> <!-- /.select-menu-item -->
        </div>

        <div class="select-menu-no-results">Nothing to show</div>
      </div> <!-- /.select-menu-list -->

    </div> <!-- /.select-menu-modal -->
  </div> <!-- /.select-menu-modal-holder -->
</div> <!-- /.select-menu -->

  <div class="breadcrumb">
    <span class='repo-root js-repo-root'><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/apache/thrift" data-branch="master" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">thrift</span></a></span></span><span class="separator"> / </span><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/apache/thrift/tree/master/lib" data-branch="master" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">lib</span></a></span><span class="separator"> / </span><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/apache/thrift/tree/master/lib/js" data-branch="master" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">js</span></a></span><span class="separator"> / </span><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/apache/thrift/tree/master/lib/js/src" data-branch="master" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">src</span></a></span><span class="separator"> / </span><strong class="final-path">thrift.js</strong> <span class="js-zeroclipboard minibutton zeroclipboard-button" data-clipboard-text="lib/js/src/thrift.js" data-copied-hint="copied!" title="copy to clipboard"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>



  <div class="commit file-history-tease">
    <img class="main-avatar" height="24" src="https://2.gravatar.com/avatar/18272c8b6b7bf949e3cb3573dc7e392c?d=https%3A%2F%2Fidenticons.github.com%2F79b28cbdcabf84cf2f5842ad4a50b300.png&amp;r=x&amp;s=140" width="24" />
    <span class="author"><a href="/henrique" rel="author">henrique</a></span>
    <time class="js-relative-date" datetime="2013-09-20T10:38:03-07:00" title="2013-09-20 10:38:03">September 20, 2013</time>
    <div class="commit-title">
        <a href="/apache/thrift/commit/095ddb7ff8c9e503c2186e8452f2de7f7451212a" class="message" data-pjax="true" title="THRIFT-2190 Add the JavaScript thrift.js lib to the Bower registry

Client: nodejs
Patch: Randy Abernethy

plus path changes">THRIFT-2190 Add the JavaScript thrift.js lib to the Bower registry</a>
    </div>

    <div class="participation">
      <p class="quickstat"><a href="#blob_contributors_box" rel="facebox"><strong>1</strong> contributor</a></p>
      
    </div>
    <div id="blob_contributors_box" style="display:none">
      <h2 class="facebox-header">Users who have contributed to this file</h2>
      <ul class="facebox-user-list">
          <li class="facebox-user-list-item">
            <img height="24" src="https://2.gravatar.com/avatar/18272c8b6b7bf949e3cb3573dc7e392c?d=https%3A%2F%2Fidenticons.github.com%2F79b28cbdcabf84cf2f5842ad4a50b300.png&amp;r=x&amp;s=140" width="24" />
            <a href="/henrique">henrique</a>
          </li>
      </ul>
    </div>
  </div>

<div id="files" class="bubble">
  <div class="file">
    <div class="meta">
      <div class="info">
        <span class="icon"><b class="octicon octicon-file-text"></b></span>
        <span class="mode" title="File Mode">file</span>
          <span>1104 lines (948 sloc)</span>
        <span>33.884 kb</span>
      </div>
      <div class="actions">
        <div class="button-group">
            <a class="minibutton tooltipped leftwards js-conduit-openfile-check"
               href="github-mac://openRepo/https://github.com/apache/thrift?branch=master&amp;filepath=lib%2Fjs%2Fsrc%2Fthrift.js"
               data-url="github-mac://openRepo/https://github.com/apache/thrift?branch=master&amp;filepath=lib%2Fjs%2Fsrc%2Fthrift.js"
               title="Open this file in GitHub for Mac"
               data-failed-title="Your version of GitHub for Mac is too old to open this file. Try checking for updates.">
                <span class="octicon octicon-device-desktop"></span> Open
            </a>
                <a class="minibutton tooltipped upwards"
                   title="Clicking this button will automatically fork this project so you can edit the file"
                   href="/apache/thrift/edit/master/lib/js/src/thrift.js"
                   data-method="post" rel="nofollow">Edit</a>
          <a href="/apache/thrift/raw/master/lib/js/src/thrift.js" class="button minibutton " id="raw-url">Raw</a>
            <a href="/apache/thrift/blame/master/lib/js/src/thrift.js" class="button minibutton ">Blame</a>
          <a href="/apache/thrift/commits/master/lib/js/src/thrift.js" class="button minibutton " rel="nofollow">History</a>
        </div><!-- /.button-group -->
          <a class="minibutton danger empty-icon tooltipped downwards"
             href="/apache/thrift/delete/master/lib/js/src/thrift.js"
             title="Fork this project and delete file"
             data-method="post" data-test-id="delete-blob-file" rel="nofollow">
          Delete
        </a>
      </div><!-- /.actions -->

    </div>
        <div class="blob-wrapper data type-javascript js-blob-data">
        <table class="file-code file-diff">
          <tr class="file-code-line">
            <td class="blob-line-nums">
              <span id="L1" rel="#L1">1</span>
<span id="L2" rel="#L2">2</span>
<span id="L3" rel="#L3">3</span>
<span id="L4" rel="#L4">4</span>
<span id="L5" rel="#L5">5</span>
<span id="L6" rel="#L6">6</span>
<span id="L7" rel="#L7">7</span>
<span id="L8" rel="#L8">8</span>
<span id="L9" rel="#L9">9</span>
<span id="L10" rel="#L10">10</span>
<span id="L11" rel="#L11">11</span>
<span id="L12" rel="#L12">12</span>
<span id="L13" rel="#L13">13</span>
<span id="L14" rel="#L14">14</span>
<span id="L15" rel="#L15">15</span>
<span id="L16" rel="#L16">16</span>
<span id="L17" rel="#L17">17</span>
<span id="L18" rel="#L18">18</span>
<span id="L19" rel="#L19">19</span>
<span id="L20" rel="#L20">20</span>
<span id="L21" rel="#L21">21</span>
<span id="L22" rel="#L22">22</span>
<span id="L23" rel="#L23">23</span>
<span id="L24" rel="#L24">24</span>
<span id="L25" rel="#L25">25</span>
<span id="L26" rel="#L26">26</span>
<span id="L27" rel="#L27">27</span>
<span id="L28" rel="#L28">28</span>
<span id="L29" rel="#L29">29</span>
<span id="L30" rel="#L30">30</span>
<span id="L31" rel="#L31">31</span>
<span id="L32" rel="#L32">32</span>
<span id="L33" rel="#L33">33</span>
<span id="L34" rel="#L34">34</span>
<span id="L35" rel="#L35">35</span>
<span id="L36" rel="#L36">36</span>
<span id="L37" rel="#L37">37</span>
<span id="L38" rel="#L38">38</span>
<span id="L39" rel="#L39">39</span>
<span id="L40" rel="#L40">40</span>
<span id="L41" rel="#L41">41</span>
<span id="L42" rel="#L42">42</span>
<span id="L43" rel="#L43">43</span>
<span id="L44" rel="#L44">44</span>
<span id="L45" rel="#L45">45</span>
<span id="L46" rel="#L46">46</span>
<span id="L47" rel="#L47">47</span>
<span id="L48" rel="#L48">48</span>
<span id="L49" rel="#L49">49</span>
<span id="L50" rel="#L50">50</span>
<span id="L51" rel="#L51">51</span>
<span id="L52" rel="#L52">52</span>
<span id="L53" rel="#L53">53</span>
<span id="L54" rel="#L54">54</span>
<span id="L55" rel="#L55">55</span>
<span id="L56" rel="#L56">56</span>
<span id="L57" rel="#L57">57</span>
<span id="L58" rel="#L58">58</span>
<span id="L59" rel="#L59">59</span>
<span id="L60" rel="#L60">60</span>
<span id="L61" rel="#L61">61</span>
<span id="L62" rel="#L62">62</span>
<span id="L63" rel="#L63">63</span>
<span id="L64" rel="#L64">64</span>
<span id="L65" rel="#L65">65</span>
<span id="L66" rel="#L66">66</span>
<span id="L67" rel="#L67">67</span>
<span id="L68" rel="#L68">68</span>
<span id="L69" rel="#L69">69</span>
<span id="L70" rel="#L70">70</span>
<span id="L71" rel="#L71">71</span>
<span id="L72" rel="#L72">72</span>
<span id="L73" rel="#L73">73</span>
<span id="L74" rel="#L74">74</span>
<span id="L75" rel="#L75">75</span>
<span id="L76" rel="#L76">76</span>
<span id="L77" rel="#L77">77</span>
<span id="L78" rel="#L78">78</span>
<span id="L79" rel="#L79">79</span>
<span id="L80" rel="#L80">80</span>
<span id="L81" rel="#L81">81</span>
<span id="L82" rel="#L82">82</span>
<span id="L83" rel="#L83">83</span>
<span id="L84" rel="#L84">84</span>
<span id="L85" rel="#L85">85</span>
<span id="L86" rel="#L86">86</span>
<span id="L87" rel="#L87">87</span>
<span id="L88" rel="#L88">88</span>
<span id="L89" rel="#L89">89</span>
<span id="L90" rel="#L90">90</span>
<span id="L91" rel="#L91">91</span>
<span id="L92" rel="#L92">92</span>
<span id="L93" rel="#L93">93</span>
<span id="L94" rel="#L94">94</span>
<span id="L95" rel="#L95">95</span>
<span id="L96" rel="#L96">96</span>
<span id="L97" rel="#L97">97</span>
<span id="L98" rel="#L98">98</span>
<span id="L99" rel="#L99">99</span>
<span id="L100" rel="#L100">100</span>
<span id="L101" rel="#L101">101</span>
<span id="L102" rel="#L102">102</span>
<span id="L103" rel="#L103">103</span>
<span id="L104" rel="#L104">104</span>
<span id="L105" rel="#L105">105</span>
<span id="L106" rel="#L106">106</span>
<span id="L107" rel="#L107">107</span>
<span id="L108" rel="#L108">108</span>
<span id="L109" rel="#L109">109</span>
<span id="L110" rel="#L110">110</span>
<span id="L111" rel="#L111">111</span>
<span id="L112" rel="#L112">112</span>
<span id="L113" rel="#L113">113</span>
<span id="L114" rel="#L114">114</span>
<span id="L115" rel="#L115">115</span>
<span id="L116" rel="#L116">116</span>
<span id="L117" rel="#L117">117</span>
<span id="L118" rel="#L118">118</span>
<span id="L119" rel="#L119">119</span>
<span id="L120" rel="#L120">120</span>
<span id="L121" rel="#L121">121</span>
<span id="L122" rel="#L122">122</span>
<span id="L123" rel="#L123">123</span>
<span id="L124" rel="#L124">124</span>
<span id="L125" rel="#L125">125</span>
<span id="L126" rel="#L126">126</span>
<span id="L127" rel="#L127">127</span>
<span id="L128" rel="#L128">128</span>
<span id="L129" rel="#L129">129</span>
<span id="L130" rel="#L130">130</span>
<span id="L131" rel="#L131">131</span>
<span id="L132" rel="#L132">132</span>
<span id="L133" rel="#L133">133</span>
<span id="L134" rel="#L134">134</span>
<span id="L135" rel="#L135">135</span>
<span id="L136" rel="#L136">136</span>
<span id="L137" rel="#L137">137</span>
<span id="L138" rel="#L138">138</span>
<span id="L139" rel="#L139">139</span>
<span id="L140" rel="#L140">140</span>
<span id="L141" rel="#L141">141</span>
<span id="L142" rel="#L142">142</span>
<span id="L143" rel="#L143">143</span>
<span id="L144" rel="#L144">144</span>
<span id="L145" rel="#L145">145</span>
<span id="L146" rel="#L146">146</span>
<span id="L147" rel="#L147">147</span>
<span id="L148" rel="#L148">148</span>
<span id="L149" rel="#L149">149</span>
<span id="L150" rel="#L150">150</span>
<span id="L151" rel="#L151">151</span>
<span id="L152" rel="#L152">152</span>
<span id="L153" rel="#L153">153</span>
<span id="L154" rel="#L154">154</span>
<span id="L155" rel="#L155">155</span>
<span id="L156" rel="#L156">156</span>
<span id="L157" rel="#L157">157</span>
<span id="L158" rel="#L158">158</span>
<span id="L159" rel="#L159">159</span>
<span id="L160" rel="#L160">160</span>
<span id="L161" rel="#L161">161</span>
<span id="L162" rel="#L162">162</span>
<span id="L163" rel="#L163">163</span>
<span id="L164" rel="#L164">164</span>
<span id="L165" rel="#L165">165</span>
<span id="L166" rel="#L166">166</span>
<span id="L167" rel="#L167">167</span>
<span id="L168" rel="#L168">168</span>
<span id="L169" rel="#L169">169</span>
<span id="L170" rel="#L170">170</span>
<span id="L171" rel="#L171">171</span>
<span id="L172" rel="#L172">172</span>
<span id="L173" rel="#L173">173</span>
<span id="L174" rel="#L174">174</span>
<span id="L175" rel="#L175">175</span>
<span id="L176" rel="#L176">176</span>
<span id="L177" rel="#L177">177</span>
<span id="L178" rel="#L178">178</span>
<span id="L179" rel="#L179">179</span>
<span id="L180" rel="#L180">180</span>
<span id="L181" rel="#L181">181</span>
<span id="L182" rel="#L182">182</span>
<span id="L183" rel="#L183">183</span>
<span id="L184" rel="#L184">184</span>
<span id="L185" rel="#L185">185</span>
<span id="L186" rel="#L186">186</span>
<span id="L187" rel="#L187">187</span>
<span id="L188" rel="#L188">188</span>
<span id="L189" rel="#L189">189</span>
<span id="L190" rel="#L190">190</span>
<span id="L191" rel="#L191">191</span>
<span id="L192" rel="#L192">192</span>
<span id="L193" rel="#L193">193</span>
<span id="L194" rel="#L194">194</span>
<span id="L195" rel="#L195">195</span>
<span id="L196" rel="#L196">196</span>
<span id="L197" rel="#L197">197</span>
<span id="L198" rel="#L198">198</span>
<span id="L199" rel="#L199">199</span>
<span id="L200" rel="#L200">200</span>
<span id="L201" rel="#L201">201</span>
<span id="L202" rel="#L202">202</span>
<span id="L203" rel="#L203">203</span>
<span id="L204" rel="#L204">204</span>
<span id="L205" rel="#L205">205</span>
<span id="L206" rel="#L206">206</span>
<span id="L207" rel="#L207">207</span>
<span id="L208" rel="#L208">208</span>
<span id="L209" rel="#L209">209</span>
<span id="L210" rel="#L210">210</span>
<span id="L211" rel="#L211">211</span>
<span id="L212" rel="#L212">212</span>
<span id="L213" rel="#L213">213</span>
<span id="L214" rel="#L214">214</span>
<span id="L215" rel="#L215">215</span>
<span id="L216" rel="#L216">216</span>
<span id="L217" rel="#L217">217</span>
<span id="L218" rel="#L218">218</span>
<span id="L219" rel="#L219">219</span>
<span id="L220" rel="#L220">220</span>
<span id="L221" rel="#L221">221</span>
<span id="L222" rel="#L222">222</span>
<span id="L223" rel="#L223">223</span>
<span id="L224" rel="#L224">224</span>
<span id="L225" rel="#L225">225</span>
<span id="L226" rel="#L226">226</span>
<span id="L227" rel="#L227">227</span>
<span id="L228" rel="#L228">228</span>
<span id="L229" rel="#L229">229</span>
<span id="L230" rel="#L230">230</span>
<span id="L231" rel="#L231">231</span>
<span id="L232" rel="#L232">232</span>
<span id="L233" rel="#L233">233</span>
<span id="L234" rel="#L234">234</span>
<span id="L235" rel="#L235">235</span>
<span id="L236" rel="#L236">236</span>
<span id="L237" rel="#L237">237</span>
<span id="L238" rel="#L238">238</span>
<span id="L239" rel="#L239">239</span>
<span id="L240" rel="#L240">240</span>
<span id="L241" rel="#L241">241</span>
<span id="L242" rel="#L242">242</span>
<span id="L243" rel="#L243">243</span>
<span id="L244" rel="#L244">244</span>
<span id="L245" rel="#L245">245</span>
<span id="L246" rel="#L246">246</span>
<span id="L247" rel="#L247">247</span>
<span id="L248" rel="#L248">248</span>
<span id="L249" rel="#L249">249</span>
<span id="L250" rel="#L250">250</span>
<span id="L251" rel="#L251">251</span>
<span id="L252" rel="#L252">252</span>
<span id="L253" rel="#L253">253</span>
<span id="L254" rel="#L254">254</span>
<span id="L255" rel="#L255">255</span>
<span id="L256" rel="#L256">256</span>
<span id="L257" rel="#L257">257</span>
<span id="L258" rel="#L258">258</span>
<span id="L259" rel="#L259">259</span>
<span id="L260" rel="#L260">260</span>
<span id="L261" rel="#L261">261</span>
<span id="L262" rel="#L262">262</span>
<span id="L263" rel="#L263">263</span>
<span id="L264" rel="#L264">264</span>
<span id="L265" rel="#L265">265</span>
<span id="L266" rel="#L266">266</span>
<span id="L267" rel="#L267">267</span>
<span id="L268" rel="#L268">268</span>
<span id="L269" rel="#L269">269</span>
<span id="L270" rel="#L270">270</span>
<span id="L271" rel="#L271">271</span>
<span id="L272" rel="#L272">272</span>
<span id="L273" rel="#L273">273</span>
<span id="L274" rel="#L274">274</span>
<span id="L275" rel="#L275">275</span>
<span id="L276" rel="#L276">276</span>
<span id="L277" rel="#L277">277</span>
<span id="L278" rel="#L278">278</span>
<span id="L279" rel="#L279">279</span>
<span id="L280" rel="#L280">280</span>
<span id="L281" rel="#L281">281</span>
<span id="L282" rel="#L282">282</span>
<span id="L283" rel="#L283">283</span>
<span id="L284" rel="#L284">284</span>
<span id="L285" rel="#L285">285</span>
<span id="L286" rel="#L286">286</span>
<span id="L287" rel="#L287">287</span>
<span id="L288" rel="#L288">288</span>
<span id="L289" rel="#L289">289</span>
<span id="L290" rel="#L290">290</span>
<span id="L291" rel="#L291">291</span>
<span id="L292" rel="#L292">292</span>
<span id="L293" rel="#L293">293</span>
<span id="L294" rel="#L294">294</span>
<span id="L295" rel="#L295">295</span>
<span id="L296" rel="#L296">296</span>
<span id="L297" rel="#L297">297</span>
<span id="L298" rel="#L298">298</span>
<span id="L299" rel="#L299">299</span>
<span id="L300" rel="#L300">300</span>
<span id="L301" rel="#L301">301</span>
<span id="L302" rel="#L302">302</span>
<span id="L303" rel="#L303">303</span>
<span id="L304" rel="#L304">304</span>
<span id="L305" rel="#L305">305</span>
<span id="L306" rel="#L306">306</span>
<span id="L307" rel="#L307">307</span>
<span id="L308" rel="#L308">308</span>
<span id="L309" rel="#L309">309</span>
<span id="L310" rel="#L310">310</span>
<span id="L311" rel="#L311">311</span>
<span id="L312" rel="#L312">312</span>
<span id="L313" rel="#L313">313</span>
<span id="L314" rel="#L314">314</span>
<span id="L315" rel="#L315">315</span>
<span id="L316" rel="#L316">316</span>
<span id="L317" rel="#L317">317</span>
<span id="L318" rel="#L318">318</span>
<span id="L319" rel="#L319">319</span>
<span id="L320" rel="#L320">320</span>
<span id="L321" rel="#L321">321</span>
<span id="L322" rel="#L322">322</span>
<span id="L323" rel="#L323">323</span>
<span id="L324" rel="#L324">324</span>
<span id="L325" rel="#L325">325</span>
<span id="L326" rel="#L326">326</span>
<span id="L327" rel="#L327">327</span>
<span id="L328" rel="#L328">328</span>
<span id="L329" rel="#L329">329</span>
<span id="L330" rel="#L330">330</span>
<span id="L331" rel="#L331">331</span>
<span id="L332" rel="#L332">332</span>
<span id="L333" rel="#L333">333</span>
<span id="L334" rel="#L334">334</span>
<span id="L335" rel="#L335">335</span>
<span id="L336" rel="#L336">336</span>
<span id="L337" rel="#L337">337</span>
<span id="L338" rel="#L338">338</span>
<span id="L339" rel="#L339">339</span>
<span id="L340" rel="#L340">340</span>
<span id="L341" rel="#L341">341</span>
<span id="L342" rel="#L342">342</span>
<span id="L343" rel="#L343">343</span>
<span id="L344" rel="#L344">344</span>
<span id="L345" rel="#L345">345</span>
<span id="L346" rel="#L346">346</span>
<span id="L347" rel="#L347">347</span>
<span id="L348" rel="#L348">348</span>
<span id="L349" rel="#L349">349</span>
<span id="L350" rel="#L350">350</span>
<span id="L351" rel="#L351">351</span>
<span id="L352" rel="#L352">352</span>
<span id="L353" rel="#L353">353</span>
<span id="L354" rel="#L354">354</span>
<span id="L355" rel="#L355">355</span>
<span id="L356" rel="#L356">356</span>
<span id="L357" rel="#L357">357</span>
<span id="L358" rel="#L358">358</span>
<span id="L359" rel="#L359">359</span>
<span id="L360" rel="#L360">360</span>
<span id="L361" rel="#L361">361</span>
<span id="L362" rel="#L362">362</span>
<span id="L363" rel="#L363">363</span>
<span id="L364" rel="#L364">364</span>
<span id="L365" rel="#L365">365</span>
<span id="L366" rel="#L366">366</span>
<span id="L367" rel="#L367">367</span>
<span id="L368" rel="#L368">368</span>
<span id="L369" rel="#L369">369</span>
<span id="L370" rel="#L370">370</span>
<span id="L371" rel="#L371">371</span>
<span id="L372" rel="#L372">372</span>
<span id="L373" rel="#L373">373</span>
<span id="L374" rel="#L374">374</span>
<span id="L375" rel="#L375">375</span>
<span id="L376" rel="#L376">376</span>
<span id="L377" rel="#L377">377</span>
<span id="L378" rel="#L378">378</span>
<span id="L379" rel="#L379">379</span>
<span id="L380" rel="#L380">380</span>
<span id="L381" rel="#L381">381</span>
<span id="L382" rel="#L382">382</span>
<span id="L383" rel="#L383">383</span>
<span id="L384" rel="#L384">384</span>
<span id="L385" rel="#L385">385</span>
<span id="L386" rel="#L386">386</span>
<span id="L387" rel="#L387">387</span>
<span id="L388" rel="#L388">388</span>
<span id="L389" rel="#L389">389</span>
<span id="L390" rel="#L390">390</span>
<span id="L391" rel="#L391">391</span>
<span id="L392" rel="#L392">392</span>
<span id="L393" rel="#L393">393</span>
<span id="L394" rel="#L394">394</span>
<span id="L395" rel="#L395">395</span>
<span id="L396" rel="#L396">396</span>
<span id="L397" rel="#L397">397</span>
<span id="L398" rel="#L398">398</span>
<span id="L399" rel="#L399">399</span>
<span id="L400" rel="#L400">400</span>
<span id="L401" rel="#L401">401</span>
<span id="L402" rel="#L402">402</span>
<span id="L403" rel="#L403">403</span>
<span id="L404" rel="#L404">404</span>
<span id="L405" rel="#L405">405</span>
<span id="L406" rel="#L406">406</span>
<span id="L407" rel="#L407">407</span>
<span id="L408" rel="#L408">408</span>
<span id="L409" rel="#L409">409</span>
<span id="L410" rel="#L410">410</span>
<span id="L411" rel="#L411">411</span>
<span id="L412" rel="#L412">412</span>
<span id="L413" rel="#L413">413</span>
<span id="L414" rel="#L414">414</span>
<span id="L415" rel="#L415">415</span>
<span id="L416" rel="#L416">416</span>
<span id="L417" rel="#L417">417</span>
<span id="L418" rel="#L418">418</span>
<span id="L419" rel="#L419">419</span>
<span id="L420" rel="#L420">420</span>
<span id="L421" rel="#L421">421</span>
<span id="L422" rel="#L422">422</span>
<span id="L423" rel="#L423">423</span>
<span id="L424" rel="#L424">424</span>
<span id="L425" rel="#L425">425</span>
<span id="L426" rel="#L426">426</span>
<span id="L427" rel="#L427">427</span>
<span id="L428" rel="#L428">428</span>
<span id="L429" rel="#L429">429</span>
<span id="L430" rel="#L430">430</span>
<span id="L431" rel="#L431">431</span>
<span id="L432" rel="#L432">432</span>
<span id="L433" rel="#L433">433</span>
<span id="L434" rel="#L434">434</span>
<span id="L435" rel="#L435">435</span>
<span id="L436" rel="#L436">436</span>
<span id="L437" rel="#L437">437</span>
<span id="L438" rel="#L438">438</span>
<span id="L439" rel="#L439">439</span>
<span id="L440" rel="#L440">440</span>
<span id="L441" rel="#L441">441</span>
<span id="L442" rel="#L442">442</span>
<span id="L443" rel="#L443">443</span>
<span id="L444" rel="#L444">444</span>
<span id="L445" rel="#L445">445</span>
<span id="L446" rel="#L446">446</span>
<span id="L447" rel="#L447">447</span>
<span id="L448" rel="#L448">448</span>
<span id="L449" rel="#L449">449</span>
<span id="L450" rel="#L450">450</span>
<span id="L451" rel="#L451">451</span>
<span id="L452" rel="#L452">452</span>
<span id="L453" rel="#L453">453</span>
<span id="L454" rel="#L454">454</span>
<span id="L455" rel="#L455">455</span>
<span id="L456" rel="#L456">456</span>
<span id="L457" rel="#L457">457</span>
<span id="L458" rel="#L458">458</span>
<span id="L459" rel="#L459">459</span>
<span id="L460" rel="#L460">460</span>
<span id="L461" rel="#L461">461</span>
<span id="L462" rel="#L462">462</span>
<span id="L463" rel="#L463">463</span>
<span id="L464" rel="#L464">464</span>
<span id="L465" rel="#L465">465</span>
<span id="L466" rel="#L466">466</span>
<span id="L467" rel="#L467">467</span>
<span id="L468" rel="#L468">468</span>
<span id="L469" rel="#L469">469</span>
<span id="L470" rel="#L470">470</span>
<span id="L471" rel="#L471">471</span>
<span id="L472" rel="#L472">472</span>
<span id="L473" rel="#L473">473</span>
<span id="L474" rel="#L474">474</span>
<span id="L475" rel="#L475">475</span>
<span id="L476" rel="#L476">476</span>
<span id="L477" rel="#L477">477</span>
<span id="L478" rel="#L478">478</span>
<span id="L479" rel="#L479">479</span>
<span id="L480" rel="#L480">480</span>
<span id="L481" rel="#L481">481</span>
<span id="L482" rel="#L482">482</span>
<span id="L483" rel="#L483">483</span>
<span id="L484" rel="#L484">484</span>
<span id="L485" rel="#L485">485</span>
<span id="L486" rel="#L486">486</span>
<span id="L487" rel="#L487">487</span>
<span id="L488" rel="#L488">488</span>
<span id="L489" rel="#L489">489</span>
<span id="L490" rel="#L490">490</span>
<span id="L491" rel="#L491">491</span>
<span id="L492" rel="#L492">492</span>
<span id="L493" rel="#L493">493</span>
<span id="L494" rel="#L494">494</span>
<span id="L495" rel="#L495">495</span>
<span id="L496" rel="#L496">496</span>
<span id="L497" rel="#L497">497</span>
<span id="L498" rel="#L498">498</span>
<span id="L499" rel="#L499">499</span>
<span id="L500" rel="#L500">500</span>
<span id="L501" rel="#L501">501</span>
<span id="L502" rel="#L502">502</span>
<span id="L503" rel="#L503">503</span>
<span id="L504" rel="#L504">504</span>
<span id="L505" rel="#L505">505</span>
<span id="L506" rel="#L506">506</span>
<span id="L507" rel="#L507">507</span>
<span id="L508" rel="#L508">508</span>
<span id="L509" rel="#L509">509</span>
<span id="L510" rel="#L510">510</span>
<span id="L511" rel="#L511">511</span>
<span id="L512" rel="#L512">512</span>
<span id="L513" rel="#L513">513</span>
<span id="L514" rel="#L514">514</span>
<span id="L515" rel="#L515">515</span>
<span id="L516" rel="#L516">516</span>
<span id="L517" rel="#L517">517</span>
<span id="L518" rel="#L518">518</span>
<span id="L519" rel="#L519">519</span>
<span id="L520" rel="#L520">520</span>
<span id="L521" rel="#L521">521</span>
<span id="L522" rel="#L522">522</span>
<span id="L523" rel="#L523">523</span>
<span id="L524" rel="#L524">524</span>
<span id="L525" rel="#L525">525</span>
<span id="L526" rel="#L526">526</span>
<span id="L527" rel="#L527">527</span>
<span id="L528" rel="#L528">528</span>
<span id="L529" rel="#L529">529</span>
<span id="L530" rel="#L530">530</span>
<span id="L531" rel="#L531">531</span>
<span id="L532" rel="#L532">532</span>
<span id="L533" rel="#L533">533</span>
<span id="L534" rel="#L534">534</span>
<span id="L535" rel="#L535">535</span>
<span id="L536" rel="#L536">536</span>
<span id="L537" rel="#L537">537</span>
<span id="L538" rel="#L538">538</span>
<span id="L539" rel="#L539">539</span>
<span id="L540" rel="#L540">540</span>
<span id="L541" rel="#L541">541</span>
<span id="L542" rel="#L542">542</span>
<span id="L543" rel="#L543">543</span>
<span id="L544" rel="#L544">544</span>
<span id="L545" rel="#L545">545</span>
<span id="L546" rel="#L546">546</span>
<span id="L547" rel="#L547">547</span>
<span id="L548" rel="#L548">548</span>
<span id="L549" rel="#L549">549</span>
<span id="L550" rel="#L550">550</span>
<span id="L551" rel="#L551">551</span>
<span id="L552" rel="#L552">552</span>
<span id="L553" rel="#L553">553</span>
<span id="L554" rel="#L554">554</span>
<span id="L555" rel="#L555">555</span>
<span id="L556" rel="#L556">556</span>
<span id="L557" rel="#L557">557</span>
<span id="L558" rel="#L558">558</span>
<span id="L559" rel="#L559">559</span>
<span id="L560" rel="#L560">560</span>
<span id="L561" rel="#L561">561</span>
<span id="L562" rel="#L562">562</span>
<span id="L563" rel="#L563">563</span>
<span id="L564" rel="#L564">564</span>
<span id="L565" rel="#L565">565</span>
<span id="L566" rel="#L566">566</span>
<span id="L567" rel="#L567">567</span>
<span id="L568" rel="#L568">568</span>
<span id="L569" rel="#L569">569</span>
<span id="L570" rel="#L570">570</span>
<span id="L571" rel="#L571">571</span>
<span id="L572" rel="#L572">572</span>
<span id="L573" rel="#L573">573</span>
<span id="L574" rel="#L574">574</span>
<span id="L575" rel="#L575">575</span>
<span id="L576" rel="#L576">576</span>
<span id="L577" rel="#L577">577</span>
<span id="L578" rel="#L578">578</span>
<span id="L579" rel="#L579">579</span>
<span id="L580" rel="#L580">580</span>
<span id="L581" rel="#L581">581</span>
<span id="L582" rel="#L582">582</span>
<span id="L583" rel="#L583">583</span>
<span id="L584" rel="#L584">584</span>
<span id="L585" rel="#L585">585</span>
<span id="L586" rel="#L586">586</span>
<span id="L587" rel="#L587">587</span>
<span id="L588" rel="#L588">588</span>
<span id="L589" rel="#L589">589</span>
<span id="L590" rel="#L590">590</span>
<span id="L591" rel="#L591">591</span>
<span id="L592" rel="#L592">592</span>
<span id="L593" rel="#L593">593</span>
<span id="L594" rel="#L594">594</span>
<span id="L595" rel="#L595">595</span>
<span id="L596" rel="#L596">596</span>
<span id="L597" rel="#L597">597</span>
<span id="L598" rel="#L598">598</span>
<span id="L599" rel="#L599">599</span>
<span id="L600" rel="#L600">600</span>
<span id="L601" rel="#L601">601</span>
<span id="L602" rel="#L602">602</span>
<span id="L603" rel="#L603">603</span>
<span id="L604" rel="#L604">604</span>
<span id="L605" rel="#L605">605</span>
<span id="L606" rel="#L606">606</span>
<span id="L607" rel="#L607">607</span>
<span id="L608" rel="#L608">608</span>
<span id="L609" rel="#L609">609</span>
<span id="L610" rel="#L610">610</span>
<span id="L611" rel="#L611">611</span>
<span id="L612" rel="#L612">612</span>
<span id="L613" rel="#L613">613</span>
<span id="L614" rel="#L614">614</span>
<span id="L615" rel="#L615">615</span>
<span id="L616" rel="#L616">616</span>
<span id="L617" rel="#L617">617</span>
<span id="L618" rel="#L618">618</span>
<span id="L619" rel="#L619">619</span>
<span id="L620" rel="#L620">620</span>
<span id="L621" rel="#L621">621</span>
<span id="L622" rel="#L622">622</span>
<span id="L623" rel="#L623">623</span>
<span id="L624" rel="#L624">624</span>
<span id="L625" rel="#L625">625</span>
<span id="L626" rel="#L626">626</span>
<span id="L627" rel="#L627">627</span>
<span id="L628" rel="#L628">628</span>
<span id="L629" rel="#L629">629</span>
<span id="L630" rel="#L630">630</span>
<span id="L631" rel="#L631">631</span>
<span id="L632" rel="#L632">632</span>
<span id="L633" rel="#L633">633</span>
<span id="L634" rel="#L634">634</span>
<span id="L635" rel="#L635">635</span>
<span id="L636" rel="#L636">636</span>
<span id="L637" rel="#L637">637</span>
<span id="L638" rel="#L638">638</span>
<span id="L639" rel="#L639">639</span>
<span id="L640" rel="#L640">640</span>
<span id="L641" rel="#L641">641</span>
<span id="L642" rel="#L642">642</span>
<span id="L643" rel="#L643">643</span>
<span id="L644" rel="#L644">644</span>
<span id="L645" rel="#L645">645</span>
<span id="L646" rel="#L646">646</span>
<span id="L647" rel="#L647">647</span>
<span id="L648" rel="#L648">648</span>
<span id="L649" rel="#L649">649</span>
<span id="L650" rel="#L650">650</span>
<span id="L651" rel="#L651">651</span>
<span id="L652" rel="#L652">652</span>
<span id="L653" rel="#L653">653</span>
<span id="L654" rel="#L654">654</span>
<span id="L655" rel="#L655">655</span>
<span id="L656" rel="#L656">656</span>
<span id="L657" rel="#L657">657</span>
<span id="L658" rel="#L658">658</span>
<span id="L659" rel="#L659">659</span>
<span id="L660" rel="#L660">660</span>
<span id="L661" rel="#L661">661</span>
<span id="L662" rel="#L662">662</span>
<span id="L663" rel="#L663">663</span>
<span id="L664" rel="#L664">664</span>
<span id="L665" rel="#L665">665</span>
<span id="L666" rel="#L666">666</span>
<span id="L667" rel="#L667">667</span>
<span id="L668" rel="#L668">668</span>
<span id="L669" rel="#L669">669</span>
<span id="L670" rel="#L670">670</span>
<span id="L671" rel="#L671">671</span>
<span id="L672" rel="#L672">672</span>
<span id="L673" rel="#L673">673</span>
<span id="L674" rel="#L674">674</span>
<span id="L675" rel="#L675">675</span>
<span id="L676" rel="#L676">676</span>
<span id="L677" rel="#L677">677</span>
<span id="L678" rel="#L678">678</span>
<span id="L679" rel="#L679">679</span>
<span id="L680" rel="#L680">680</span>
<span id="L681" rel="#L681">681</span>
<span id="L682" rel="#L682">682</span>
<span id="L683" rel="#L683">683</span>
<span id="L684" rel="#L684">684</span>
<span id="L685" rel="#L685">685</span>
<span id="L686" rel="#L686">686</span>
<span id="L687" rel="#L687">687</span>
<span id="L688" rel="#L688">688</span>
<span id="L689" rel="#L689">689</span>
<span id="L690" rel="#L690">690</span>
<span id="L691" rel="#L691">691</span>
<span id="L692" rel="#L692">692</span>
<span id="L693" rel="#L693">693</span>
<span id="L694" rel="#L694">694</span>
<span id="L695" rel="#L695">695</span>
<span id="L696" rel="#L696">696</span>
<span id="L697" rel="#L697">697</span>
<span id="L698" rel="#L698">698</span>
<span id="L699" rel="#L699">699</span>
<span id="L700" rel="#L700">700</span>
<span id="L701" rel="#L701">701</span>
<span id="L702" rel="#L702">702</span>
<span id="L703" rel="#L703">703</span>
<span id="L704" rel="#L704">704</span>
<span id="L705" rel="#L705">705</span>
<span id="L706" rel="#L706">706</span>
<span id="L707" rel="#L707">707</span>
<span id="L708" rel="#L708">708</span>
<span id="L709" rel="#L709">709</span>
<span id="L710" rel="#L710">710</span>
<span id="L711" rel="#L711">711</span>
<span id="L712" rel="#L712">712</span>
<span id="L713" rel="#L713">713</span>
<span id="L714" rel="#L714">714</span>
<span id="L715" rel="#L715">715</span>
<span id="L716" rel="#L716">716</span>
<span id="L717" rel="#L717">717</span>
<span id="L718" rel="#L718">718</span>
<span id="L719" rel="#L719">719</span>
<span id="L720" rel="#L720">720</span>
<span id="L721" rel="#L721">721</span>
<span id="L722" rel="#L722">722</span>
<span id="L723" rel="#L723">723</span>
<span id="L724" rel="#L724">724</span>
<span id="L725" rel="#L725">725</span>
<span id="L726" rel="#L726">726</span>
<span id="L727" rel="#L727">727</span>
<span id="L728" rel="#L728">728</span>
<span id="L729" rel="#L729">729</span>
<span id="L730" rel="#L730">730</span>
<span id="L731" rel="#L731">731</span>
<span id="L732" rel="#L732">732</span>
<span id="L733" rel="#L733">733</span>
<span id="L734" rel="#L734">734</span>
<span id="L735" rel="#L735">735</span>
<span id="L736" rel="#L736">736</span>
<span id="L737" rel="#L737">737</span>
<span id="L738" rel="#L738">738</span>
<span id="L739" rel="#L739">739</span>
<span id="L740" rel="#L740">740</span>
<span id="L741" rel="#L741">741</span>
<span id="L742" rel="#L742">742</span>
<span id="L743" rel="#L743">743</span>
<span id="L744" rel="#L744">744</span>
<span id="L745" rel="#L745">745</span>
<span id="L746" rel="#L746">746</span>
<span id="L747" rel="#L747">747</span>
<span id="L748" rel="#L748">748</span>
<span id="L749" rel="#L749">749</span>
<span id="L750" rel="#L750">750</span>
<span id="L751" rel="#L751">751</span>
<span id="L752" rel="#L752">752</span>
<span id="L753" rel="#L753">753</span>
<span id="L754" rel="#L754">754</span>
<span id="L755" rel="#L755">755</span>
<span id="L756" rel="#L756">756</span>
<span id="L757" rel="#L757">757</span>
<span id="L758" rel="#L758">758</span>
<span id="L759" rel="#L759">759</span>
<span id="L760" rel="#L760">760</span>
<span id="L761" rel="#L761">761</span>
<span id="L762" rel="#L762">762</span>
<span id="L763" rel="#L763">763</span>
<span id="L764" rel="#L764">764</span>
<span id="L765" rel="#L765">765</span>
<span id="L766" rel="#L766">766</span>
<span id="L767" rel="#L767">767</span>
<span id="L768" rel="#L768">768</span>
<span id="L769" rel="#L769">769</span>
<span id="L770" rel="#L770">770</span>
<span id="L771" rel="#L771">771</span>
<span id="L772" rel="#L772">772</span>
<span id="L773" rel="#L773">773</span>
<span id="L774" rel="#L774">774</span>
<span id="L775" rel="#L775">775</span>
<span id="L776" rel="#L776">776</span>
<span id="L777" rel="#L777">777</span>
<span id="L778" rel="#L778">778</span>
<span id="L779" rel="#L779">779</span>
<span id="L780" rel="#L780">780</span>
<span id="L781" rel="#L781">781</span>
<span id="L782" rel="#L782">782</span>
<span id="L783" rel="#L783">783</span>
<span id="L784" rel="#L784">784</span>
<span id="L785" rel="#L785">785</span>
<span id="L786" rel="#L786">786</span>
<span id="L787" rel="#L787">787</span>
<span id="L788" rel="#L788">788</span>
<span id="L789" rel="#L789">789</span>
<span id="L790" rel="#L790">790</span>
<span id="L791" rel="#L791">791</span>
<span id="L792" rel="#L792">792</span>
<span id="L793" rel="#L793">793</span>
<span id="L794" rel="#L794">794</span>
<span id="L795" rel="#L795">795</span>
<span id="L796" rel="#L796">796</span>
<span id="L797" rel="#L797">797</span>
<span id="L798" rel="#L798">798</span>
<span id="L799" rel="#L799">799</span>
<span id="L800" rel="#L800">800</span>
<span id="L801" rel="#L801">801</span>
<span id="L802" rel="#L802">802</span>
<span id="L803" rel="#L803">803</span>
<span id="L804" rel="#L804">804</span>
<span id="L805" rel="#L805">805</span>
<span id="L806" rel="#L806">806</span>
<span id="L807" rel="#L807">807</span>
<span id="L808" rel="#L808">808</span>
<span id="L809" rel="#L809">809</span>
<span id="L810" rel="#L810">810</span>
<span id="L811" rel="#L811">811</span>
<span id="L812" rel="#L812">812</span>
<span id="L813" rel="#L813">813</span>
<span id="L814" rel="#L814">814</span>
<span id="L815" rel="#L815">815</span>
<span id="L816" rel="#L816">816</span>
<span id="L817" rel="#L817">817</span>
<span id="L818" rel="#L818">818</span>
<span id="L819" rel="#L819">819</span>
<span id="L820" rel="#L820">820</span>
<span id="L821" rel="#L821">821</span>
<span id="L822" rel="#L822">822</span>
<span id="L823" rel="#L823">823</span>
<span id="L824" rel="#L824">824</span>
<span id="L825" rel="#L825">825</span>
<span id="L826" rel="#L826">826</span>
<span id="L827" rel="#L827">827</span>
<span id="L828" rel="#L828">828</span>
<span id="L829" rel="#L829">829</span>
<span id="L830" rel="#L830">830</span>
<span id="L831" rel="#L831">831</span>
<span id="L832" rel="#L832">832</span>
<span id="L833" rel="#L833">833</span>
<span id="L834" rel="#L834">834</span>
<span id="L835" rel="#L835">835</span>
<span id="L836" rel="#L836">836</span>
<span id="L837" rel="#L837">837</span>
<span id="L838" rel="#L838">838</span>
<span id="L839" rel="#L839">839</span>
<span id="L840" rel="#L840">840</span>
<span id="L841" rel="#L841">841</span>
<span id="L842" rel="#L842">842</span>
<span id="L843" rel="#L843">843</span>
<span id="L844" rel="#L844">844</span>
<span id="L845" rel="#L845">845</span>
<span id="L846" rel="#L846">846</span>
<span id="L847" rel="#L847">847</span>
<span id="L848" rel="#L848">848</span>
<span id="L849" rel="#L849">849</span>
<span id="L850" rel="#L850">850</span>
<span id="L851" rel="#L851">851</span>
<span id="L852" rel="#L852">852</span>
<span id="L853" rel="#L853">853</span>
<span id="L854" rel="#L854">854</span>
<span id="L855" rel="#L855">855</span>
<span id="L856" rel="#L856">856</span>
<span id="L857" rel="#L857">857</span>
<span id="L858" rel="#L858">858</span>
<span id="L859" rel="#L859">859</span>
<span id="L860" rel="#L860">860</span>
<span id="L861" rel="#L861">861</span>
<span id="L862" rel="#L862">862</span>
<span id="L863" rel="#L863">863</span>
<span id="L864" rel="#L864">864</span>
<span id="L865" rel="#L865">865</span>
<span id="L866" rel="#L866">866</span>
<span id="L867" rel="#L867">867</span>
<span id="L868" rel="#L868">868</span>
<span id="L869" rel="#L869">869</span>
<span id="L870" rel="#L870">870</span>
<span id="L871" rel="#L871">871</span>
<span id="L872" rel="#L872">872</span>
<span id="L873" rel="#L873">873</span>
<span id="L874" rel="#L874">874</span>
<span id="L875" rel="#L875">875</span>
<span id="L876" rel="#L876">876</span>
<span id="L877" rel="#L877">877</span>
<span id="L878" rel="#L878">878</span>
<span id="L879" rel="#L879">879</span>
<span id="L880" rel="#L880">880</span>
<span id="L881" rel="#L881">881</span>
<span id="L882" rel="#L882">882</span>
<span id="L883" rel="#L883">883</span>
<span id="L884" rel="#L884">884</span>
<span id="L885" rel="#L885">885</span>
<span id="L886" rel="#L886">886</span>
<span id="L887" rel="#L887">887</span>
<span id="L888" rel="#L888">888</span>
<span id="L889" rel="#L889">889</span>
<span id="L890" rel="#L890">890</span>
<span id="L891" rel="#L891">891</span>
<span id="L892" rel="#L892">892</span>
<span id="L893" rel="#L893">893</span>
<span id="L894" rel="#L894">894</span>
<span id="L895" rel="#L895">895</span>
<span id="L896" rel="#L896">896</span>
<span id="L897" rel="#L897">897</span>
<span id="L898" rel="#L898">898</span>
<span id="L899" rel="#L899">899</span>
<span id="L900" rel="#L900">900</span>
<span id="L901" rel="#L901">901</span>
<span id="L902" rel="#L902">902</span>
<span id="L903" rel="#L903">903</span>
<span id="L904" rel="#L904">904</span>
<span id="L905" rel="#L905">905</span>
<span id="L906" rel="#L906">906</span>
<span id="L907" rel="#L907">907</span>
<span id="L908" rel="#L908">908</span>
<span id="L909" rel="#L909">909</span>
<span id="L910" rel="#L910">910</span>
<span id="L911" rel="#L911">911</span>
<span id="L912" rel="#L912">912</span>
<span id="L913" rel="#L913">913</span>
<span id="L914" rel="#L914">914</span>
<span id="L915" rel="#L915">915</span>
<span id="L916" rel="#L916">916</span>
<span id="L917" rel="#L917">917</span>
<span id="L918" rel="#L918">918</span>
<span id="L919" rel="#L919">919</span>
<span id="L920" rel="#L920">920</span>
<span id="L921" rel="#L921">921</span>
<span id="L922" rel="#L922">922</span>
<span id="L923" rel="#L923">923</span>
<span id="L924" rel="#L924">924</span>
<span id="L925" rel="#L925">925</span>
<span id="L926" rel="#L926">926</span>
<span id="L927" rel="#L927">927</span>
<span id="L928" rel="#L928">928</span>
<span id="L929" rel="#L929">929</span>
<span id="L930" rel="#L930">930</span>
<span id="L931" rel="#L931">931</span>
<span id="L932" rel="#L932">932</span>
<span id="L933" rel="#L933">933</span>
<span id="L934" rel="#L934">934</span>
<span id="L935" rel="#L935">935</span>
<span id="L936" rel="#L936">936</span>
<span id="L937" rel="#L937">937</span>
<span id="L938" rel="#L938">938</span>
<span id="L939" rel="#L939">939</span>
<span id="L940" rel="#L940">940</span>
<span id="L941" rel="#L941">941</span>
<span id="L942" rel="#L942">942</span>
<span id="L943" rel="#L943">943</span>
<span id="L944" rel="#L944">944</span>
<span id="L945" rel="#L945">945</span>
<span id="L946" rel="#L946">946</span>
<span id="L947" rel="#L947">947</span>
<span id="L948" rel="#L948">948</span>
<span id="L949" rel="#L949">949</span>
<span id="L950" rel="#L950">950</span>
<span id="L951" rel="#L951">951</span>
<span id="L952" rel="#L952">952</span>
<span id="L953" rel="#L953">953</span>
<span id="L954" rel="#L954">954</span>
<span id="L955" rel="#L955">955</span>
<span id="L956" rel="#L956">956</span>
<span id="L957" rel="#L957">957</span>
<span id="L958" rel="#L958">958</span>
<span id="L959" rel="#L959">959</span>
<span id="L960" rel="#L960">960</span>
<span id="L961" rel="#L961">961</span>
<span id="L962" rel="#L962">962</span>
<span id="L963" rel="#L963">963</span>
<span id="L964" rel="#L964">964</span>
<span id="L965" rel="#L965">965</span>
<span id="L966" rel="#L966">966</span>
<span id="L967" rel="#L967">967</span>
<span id="L968" rel="#L968">968</span>
<span id="L969" rel="#L969">969</span>
<span id="L970" rel="#L970">970</span>
<span id="L971" rel="#L971">971</span>
<span id="L972" rel="#L972">972</span>
<span id="L973" rel="#L973">973</span>
<span id="L974" rel="#L974">974</span>
<span id="L975" rel="#L975">975</span>
<span id="L976" rel="#L976">976</span>
<span id="L977" rel="#L977">977</span>
<span id="L978" rel="#L978">978</span>
<span id="L979" rel="#L979">979</span>
<span id="L980" rel="#L980">980</span>
<span id="L981" rel="#L981">981</span>
<span id="L982" rel="#L982">982</span>
<span id="L983" rel="#L983">983</span>
<span id="L984" rel="#L984">984</span>
<span id="L985" rel="#L985">985</span>
<span id="L986" rel="#L986">986</span>
<span id="L987" rel="#L987">987</span>
<span id="L988" rel="#L988">988</span>
<span id="L989" rel="#L989">989</span>
<span id="L990" rel="#L990">990</span>
<span id="L991" rel="#L991">991</span>
<span id="L992" rel="#L992">992</span>
<span id="L993" rel="#L993">993</span>
<span id="L994" rel="#L994">994</span>
<span id="L995" rel="#L995">995</span>
<span id="L996" rel="#L996">996</span>
<span id="L997" rel="#L997">997</span>
<span id="L998" rel="#L998">998</span>
<span id="L999" rel="#L999">999</span>
<span id="L1000" rel="#L1000">1000</span>
<span id="L1001" rel="#L1001">1001</span>
<span id="L1002" rel="#L1002">1002</span>
<span id="L1003" rel="#L1003">1003</span>
<span id="L1004" rel="#L1004">1004</span>
<span id="L1005" rel="#L1005">1005</span>
<span id="L1006" rel="#L1006">1006</span>
<span id="L1007" rel="#L1007">1007</span>
<span id="L1008" rel="#L1008">1008</span>
<span id="L1009" rel="#L1009">1009</span>
<span id="L1010" rel="#L1010">1010</span>
<span id="L1011" rel="#L1011">1011</span>
<span id="L1012" rel="#L1012">1012</span>
<span id="L1013" rel="#L1013">1013</span>
<span id="L1014" rel="#L1014">1014</span>
<span id="L1015" rel="#L1015">1015</span>
<span id="L1016" rel="#L1016">1016</span>
<span id="L1017" rel="#L1017">1017</span>
<span id="L1018" rel="#L1018">1018</span>
<span id="L1019" rel="#L1019">1019</span>
<span id="L1020" rel="#L1020">1020</span>
<span id="L1021" rel="#L1021">1021</span>
<span id="L1022" rel="#L1022">1022</span>
<span id="L1023" rel="#L1023">1023</span>
<span id="L1024" rel="#L1024">1024</span>
<span id="L1025" rel="#L1025">1025</span>
<span id="L1026" rel="#L1026">1026</span>
<span id="L1027" rel="#L1027">1027</span>
<span id="L1028" rel="#L1028">1028</span>
<span id="L1029" rel="#L1029">1029</span>
<span id="L1030" rel="#L1030">1030</span>
<span id="L1031" rel="#L1031">1031</span>
<span id="L1032" rel="#L1032">1032</span>
<span id="L1033" rel="#L1033">1033</span>
<span id="L1034" rel="#L1034">1034</span>
<span id="L1035" rel="#L1035">1035</span>
<span id="L1036" rel="#L1036">1036</span>
<span id="L1037" rel="#L1037">1037</span>
<span id="L1038" rel="#L1038">1038</span>
<span id="L1039" rel="#L1039">1039</span>
<span id="L1040" rel="#L1040">1040</span>
<span id="L1041" rel="#L1041">1041</span>
<span id="L1042" rel="#L1042">1042</span>
<span id="L1043" rel="#L1043">1043</span>
<span id="L1044" rel="#L1044">1044</span>
<span id="L1045" rel="#L1045">1045</span>
<span id="L1046" rel="#L1046">1046</span>
<span id="L1047" rel="#L1047">1047</span>
<span id="L1048" rel="#L1048">1048</span>
<span id="L1049" rel="#L1049">1049</span>
<span id="L1050" rel="#L1050">1050</span>
<span id="L1051" rel="#L1051">1051</span>
<span id="L1052" rel="#L1052">1052</span>
<span id="L1053" rel="#L1053">1053</span>
<span id="L1054" rel="#L1054">1054</span>
<span id="L1055" rel="#L1055">1055</span>
<span id="L1056" rel="#L1056">1056</span>
<span id="L1057" rel="#L1057">1057</span>
<span id="L1058" rel="#L1058">1058</span>
<span id="L1059" rel="#L1059">1059</span>
<span id="L1060" rel="#L1060">1060</span>
<span id="L1061" rel="#L1061">1061</span>
<span id="L1062" rel="#L1062">1062</span>
<span id="L1063" rel="#L1063">1063</span>
<span id="L1064" rel="#L1064">1064</span>
<span id="L1065" rel="#L1065">1065</span>
<span id="L1066" rel="#L1066">1066</span>
<span id="L1067" rel="#L1067">1067</span>
<span id="L1068" rel="#L1068">1068</span>
<span id="L1069" rel="#L1069">1069</span>
<span id="L1070" rel="#L1070">1070</span>
<span id="L1071" rel="#L1071">1071</span>
<span id="L1072" rel="#L1072">1072</span>
<span id="L1073" rel="#L1073">1073</span>
<span id="L1074" rel="#L1074">1074</span>
<span id="L1075" rel="#L1075">1075</span>
<span id="L1076" rel="#L1076">1076</span>
<span id="L1077" rel="#L1077">1077</span>
<span id="L1078" rel="#L1078">1078</span>
<span id="L1079" rel="#L1079">1079</span>
<span id="L1080" rel="#L1080">1080</span>
<span id="L1081" rel="#L1081">1081</span>
<span id="L1082" rel="#L1082">1082</span>
<span id="L1083" rel="#L1083">1083</span>
<span id="L1084" rel="#L1084">1084</span>
<span id="L1085" rel="#L1085">1085</span>
<span id="L1086" rel="#L1086">1086</span>
<span id="L1087" rel="#L1087">1087</span>
<span id="L1088" rel="#L1088">1088</span>
<span id="L1089" rel="#L1089">1089</span>
<span id="L1090" rel="#L1090">1090</span>
<span id="L1091" rel="#L1091">1091</span>
<span id="L1092" rel="#L1092">1092</span>
<span id="L1093" rel="#L1093">1093</span>
<span id="L1094" rel="#L1094">1094</span>
<span id="L1095" rel="#L1095">1095</span>
<span id="L1096" rel="#L1096">1096</span>
<span id="L1097" rel="#L1097">1097</span>
<span id="L1098" rel="#L1098">1098</span>
<span id="L1099" rel="#L1099">1099</span>
<span id="L1100" rel="#L1100">1100</span>
<span id="L1101" rel="#L1101">1101</span>
<span id="L1102" rel="#L1102">1102</span>
<span id="L1103" rel="#L1103">1103</span>

            </td>
            <td class="blob-line-code">
                    <div class="highlight"><pre><div class='line' id='LC1'><span class="cm">/*</span></div><div class='line' id='LC2'><span class="cm"> * Licensed to the Apache Software Foundation (ASF) under one</span></div><div class='line' id='LC3'><span class="cm"> * or more contributor license agreements. See the NOTICE file</span></div><div class='line' id='LC4'><span class="cm"> * distributed with this work for additional information</span></div><div class='line' id='LC5'><span class="cm"> * regarding copyright ownership. The ASF licenses this file</span></div><div class='line' id='LC6'><span class="cm"> * to you under the Apache License, Version 2.0 (the</span></div><div class='line' id='LC7'><span class="cm"> * &quot;License&quot;); you may not use this file except in compliance</span></div><div class='line' id='LC8'><span class="cm"> * with the License. You may obtain a copy of the License at</span></div><div class='line' id='LC9'><span class="cm"> *</span></div><div class='line' id='LC10'><span class="cm"> *   http://www.apache.org/licenses/LICENSE-2.0</span></div><div class='line' id='LC11'><span class="cm"> *</span></div><div class='line' id='LC12'><span class="cm"> * Unless required by applicable law or agreed to in writing,</span></div><div class='line' id='LC13'><span class="cm"> * software distributed under the License is distributed on an</span></div><div class='line' id='LC14'><span class="cm"> * &quot;AS IS&quot; BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY</span></div><div class='line' id='LC15'><span class="cm"> * KIND, either express or implied. See the License for the</span></div><div class='line' id='LC16'><span class="cm"> * specific language governing permissions and limitations</span></div><div class='line' id='LC17'><span class="cm"> * under the License.</span></div><div class='line' id='LC18'><span class="cm"> */</span></div><div class='line' id='LC19'><br/></div><div class='line' id='LC20'><span class="cm">/*jshint evil:true*/</span></div><div class='line' id='LC21'><br/></div><div class='line' id='LC22'><span class="cm">/**</span></div><div class='line' id='LC23'><span class="cm"> * The Thrift namespace houses the Apache Thrift JavaScript library </span></div><div class='line' id='LC24'><span class="cm"> * elements providing JavaScript bindings for the Apache Thrift RPC </span></div><div class='line' id='LC25'><span class="cm"> * system. Users will typically only directly make use of the </span></div><div class='line' id='LC26'><span class="cm"> * Transport and Protocol constructors.</span></div><div class='line' id='LC27'><span class="cm"> * @namespace</span></div><div class='line' id='LC28'><span class="cm"> * @example</span></div><div class='line' id='LC29'><span class="cm"> *     var transport = new Thrift.Transport(&quot;http://localhost:8585&quot;);</span></div><div class='line' id='LC30'><span class="cm"> *     var protocol  = new Thrift.Protocol(transport);</span></div><div class='line' id='LC31'><span class="cm"> *     var client = new MyThriftSvcClient(protocol);</span></div><div class='line' id='LC32'><span class="cm"> *     var result = client.MyMethod();</span></div><div class='line' id='LC33'><span class="cm"> */</span></div><div class='line' id='LC34'><span class="kd">var</span> <span class="nx">Thrift</span> <span class="o">=</span> <span class="p">{</span></div><div class='line' id='LC35'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC36'><span class="cm">     * Thrift JavaScript library version.</span></div><div class='line' id='LC37'><span class="cm">     * @readonly</span></div><div class='line' id='LC38'><span class="cm">     * @const {string} Version</span></div><div class='line' id='LC39'><span class="cm">     * @memberof Thrift</span></div><div class='line' id='LC40'><span class="cm">     */</span></div><div class='line' id='LC41'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">Version</span><span class="o">:</span> <span class="s1">&#39;1.0.0-dev&#39;</span><span class="p">,</span></div><div class='line' id='LC42'><br/></div><div class='line' id='LC43'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC44'><span class="cm">     * Thrift IDL type string to Id mapping.</span></div><div class='line' id='LC45'><span class="cm">     * @readonly</span></div><div class='line' id='LC46'><span class="cm">     * @property {number}  STOP   - End of a set of fields.</span></div><div class='line' id='LC47'><span class="cm">     * @property {number}  VOID   - No value (only legal for return types).</span></div><div class='line' id='LC48'><span class="cm">     * @property {number}  BOOL   - True/False integer.</span></div><div class='line' id='LC49'><span class="cm">     * @property {number}  BYTE   - Signed 8 bit integer.</span></div><div class='line' id='LC50'><span class="cm">     * @property {number}  I08    - Signed 8 bit integer.     </span></div><div class='line' id='LC51'><span class="cm">     * @property {number}  DOUBLE - 64 bit IEEE 854 floating point.</span></div><div class='line' id='LC52'><span class="cm">     * @property {number}  I16    - Signed 16 bit integer.</span></div><div class='line' id='LC53'><span class="cm">     * @property {number}  I32    - Signed 32 bit integer.</span></div><div class='line' id='LC54'><span class="cm">     * @property {number}  I64    - Signed 64 bit integer.</span></div><div class='line' id='LC55'><span class="cm">     * @property {number}  STRING - Array of bytes representing a string of characters.</span></div><div class='line' id='LC56'><span class="cm">     * @property {number}  UTF7   - Array of bytes representing a string of UTF7 encoded characters.</span></div><div class='line' id='LC57'><span class="cm">     * @property {number}  STRUCT - A multifield type.</span></div><div class='line' id='LC58'><span class="cm">     * @property {number}  MAP    - A collection type (map/associative-array/dictionary).</span></div><div class='line' id='LC59'><span class="cm">     * @property {number}  SET    - A collection type (unordered and without repeated values).</span></div><div class='line' id='LC60'><span class="cm">     * @property {number}  LIST   - A collection type (unordered).</span></div><div class='line' id='LC61'><span class="cm">     * @property {number}  UTF8   - Array of bytes representing a string of UTF8 encoded characters.</span></div><div class='line' id='LC62'><span class="cm">     * @property {number}  UTF16  - Array of bytes representing a string of UTF16 encoded characters.</span></div><div class='line' id='LC63'><span class="cm">     */</span></div><div class='line' id='LC64'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">Type</span><span class="o">:</span> <span class="p">{</span></div><div class='line' id='LC65'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;STOP&#39;</span> <span class="o">:</span> <span class="mi">0</span><span class="p">,</span></div><div class='line' id='LC66'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;VOID&#39;</span> <span class="o">:</span> <span class="mi">1</span><span class="p">,</span></div><div class='line' id='LC67'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;BOOL&#39;</span> <span class="o">:</span> <span class="mi">2</span><span class="p">,</span></div><div class='line' id='LC68'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;BYTE&#39;</span> <span class="o">:</span> <span class="mi">3</span><span class="p">,</span></div><div class='line' id='LC69'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;I08&#39;</span> <span class="o">:</span> <span class="mi">3</span><span class="p">,</span></div><div class='line' id='LC70'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;DOUBLE&#39;</span> <span class="o">:</span> <span class="mi">4</span><span class="p">,</span></div><div class='line' id='LC71'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;I16&#39;</span> <span class="o">:</span> <span class="mi">6</span><span class="p">,</span></div><div class='line' id='LC72'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;I32&#39;</span> <span class="o">:</span> <span class="mi">8</span><span class="p">,</span></div><div class='line' id='LC73'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;I64&#39;</span> <span class="o">:</span> <span class="mi">10</span><span class="p">,</span></div><div class='line' id='LC74'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;STRING&#39;</span> <span class="o">:</span> <span class="mi">11</span><span class="p">,</span></div><div class='line' id='LC75'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;UTF7&#39;</span> <span class="o">:</span> <span class="mi">11</span><span class="p">,</span></div><div class='line' id='LC76'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;STRUCT&#39;</span> <span class="o">:</span> <span class="mi">12</span><span class="p">,</span></div><div class='line' id='LC77'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;MAP&#39;</span> <span class="o">:</span> <span class="mi">13</span><span class="p">,</span></div><div class='line' id='LC78'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;SET&#39;</span> <span class="o">:</span> <span class="mi">14</span><span class="p">,</span></div><div class='line' id='LC79'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;LIST&#39;</span> <span class="o">:</span> <span class="mi">15</span><span class="p">,</span></div><div class='line' id='LC80'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;UTF8&#39;</span> <span class="o">:</span> <span class="mi">16</span><span class="p">,</span></div><div class='line' id='LC81'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;UTF16&#39;</span> <span class="o">:</span> <span class="mi">17</span></div><div class='line' id='LC82'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC83'><br/></div><div class='line' id='LC84'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC85'><span class="cm">     * Thrift RPC message type string to Id mapping.</span></div><div class='line' id='LC86'><span class="cm">     * @readonly</span></div><div class='line' id='LC87'><span class="cm">     * @property {number}  CALL      - RPC call sent from client to server.</span></div><div class='line' id='LC88'><span class="cm">     * @property {number}  REPLY     - RPC call normal response from server to client.</span></div><div class='line' id='LC89'><span class="cm">     * @property {number}  EXCEPTION - RPC call exception response from server to client.</span></div><div class='line' id='LC90'><span class="cm">     * @property {number}  ONEWAY    - Oneway RPC call from client to server with no response.</span></div><div class='line' id='LC91'><span class="cm">     */</span></div><div class='line' id='LC92'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">MessageType</span><span class="o">:</span> <span class="p">{</span></div><div class='line' id='LC93'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;CALL&#39;</span> <span class="o">:</span> <span class="mi">1</span><span class="p">,</span></div><div class='line' id='LC94'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;REPLY&#39;</span> <span class="o">:</span> <span class="mi">2</span><span class="p">,</span></div><div class='line' id='LC95'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;EXCEPTION&#39;</span> <span class="o">:</span> <span class="mi">3</span><span class="p">,</span></div><div class='line' id='LC96'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;ONEWAY&#39;</span> <span class="o">:</span> <span class="mi">4</span></div><div class='line' id='LC97'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC98'><br/></div><div class='line' id='LC99'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC100'><span class="cm">     * Utility function returning the count of an object&#39;s own properties.</span></div><div class='line' id='LC101'><span class="cm">     * @param {object} obj - Object to test.</span></div><div class='line' id='LC102'><span class="cm">     * @returns {number} number of object&#39;s own properties</span></div><div class='line' id='LC103'><span class="cm">     */</span></div><div class='line' id='LC104'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">objectLength</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">obj</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC105'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">length</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span></div><div class='line' id='LC106'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">for</span> <span class="p">(</span><span class="kd">var</span> <span class="nx">k</span> <span class="k">in</span> <span class="nx">obj</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC107'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">obj</span><span class="p">.</span><span class="nx">hasOwnProperty</span><span class="p">(</span><span class="nx">k</span><span class="p">))</span> <span class="p">{</span></div><div class='line' id='LC108'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">length</span><span class="o">++</span><span class="p">;</span></div><div class='line' id='LC109'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC110'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC111'><br/></div><div class='line' id='LC112'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nx">length</span><span class="p">;</span></div><div class='line' id='LC113'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC114'><br/></div><div class='line' id='LC115'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC116'><span class="cm">     * Utility function to establish prototype inheritance.</span></div><div class='line' id='LC117'><span class="cm">     * @see {@link http://javascript.crockford.com/prototypal.html|Prototypal Inheritance}</span></div><div class='line' id='LC118'><span class="cm">     * @param {function} constructor - Contstructor function to set as derived.</span></div><div class='line' id='LC119'><span class="cm">     * @param {function} superConstructor - Contstructor function to set as base.</span></div><div class='line' id='LC120'><span class="cm">     * @param {string} [name] - Type name to set as name property in derived prototype.</span></div><div class='line' id='LC121'><span class="cm">     */</span></div><div class='line' id='LC122'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">inherits</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">constructor</span><span class="p">,</span> <span class="nx">superConstructor</span><span class="p">,</span> <span class="nx">name</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC123'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">F</span><span class="p">()</span> <span class="p">{}</span></div><div class='line' id='LC124'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">F</span><span class="p">.</span><span class="nx">prototype</span> <span class="o">=</span> <span class="nx">superConstructor</span><span class="p">.</span><span class="nx">prototype</span><span class="p">;</span></div><div class='line' id='LC125'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">constructor</span><span class="p">.</span><span class="nx">prototype</span> <span class="o">=</span> <span class="k">new</span> <span class="nx">F</span><span class="p">();</span></div><div class='line' id='LC126'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">constructor</span><span class="p">.</span><span class="nx">prototype</span><span class="p">.</span><span class="nx">name</span> <span class="o">=</span> <span class="nx">name</span> <span class="o">||</span> <span class="s2">&quot;&quot;</span><span class="p">;</span></div><div class='line' id='LC127'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC128'><span class="p">};</span></div><div class='line' id='LC129'><br/></div><div class='line' id='LC130'><span class="cm">/**</span></div><div class='line' id='LC131'><span class="cm"> * Initializes a Thrift TException instance.</span></div><div class='line' id='LC132'><span class="cm"> * @constructor</span></div><div class='line' id='LC133'><span class="cm"> * @augments Error</span></div><div class='line' id='LC134'><span class="cm"> * @param {string} message - The TException message (distinct from the Error message).</span></div><div class='line' id='LC135'><span class="cm"> * @classdesc TException is the base class for all Thrift exceptions types.</span></div><div class='line' id='LC136'><span class="cm"> */</span></div><div class='line' id='LC137'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">TException</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">message</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC138'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">message</span> <span class="o">=</span> <span class="nx">message</span><span class="p">;</span></div><div class='line' id='LC139'><span class="p">};</span></div><div class='line' id='LC140'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">inherits</span><span class="p">(</span><span class="nx">Thrift</span><span class="p">.</span><span class="nx">TException</span><span class="p">,</span> <span class="nb">Error</span><span class="p">,</span> <span class="s1">&#39;TException&#39;</span><span class="p">);</span></div><div class='line' id='LC141'><br/></div><div class='line' id='LC142'><span class="cm">/**</span></div><div class='line' id='LC143'><span class="cm"> * Returns the message set on the exception.</span></div><div class='line' id='LC144'><span class="cm"> * @readonly</span></div><div class='line' id='LC145'><span class="cm"> * @returns {string} exception message</span></div><div class='line' id='LC146'><span class="cm"> */</span></div><div class='line' id='LC147'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">TException</span><span class="p">.</span><span class="nx">prototype</span><span class="p">.</span><span class="nx">getMessage</span> <span class="o">=</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC148'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="k">this</span><span class="p">.</span><span class="nx">message</span><span class="p">;</span></div><div class='line' id='LC149'><span class="p">};</span></div><div class='line' id='LC150'><br/></div><div class='line' id='LC151'><span class="cm">/**</span></div><div class='line' id='LC152'><span class="cm"> * Thrift Application Exception type string to Id mapping.</span></div><div class='line' id='LC153'><span class="cm"> * @readonly</span></div><div class='line' id='LC154'><span class="cm"> * @property {number}  UNKNOWN                 - Unknown/undefined.</span></div><div class='line' id='LC155'><span class="cm"> * @property {number}  UNKNOWN_METHOD          - Client attempted to call a method unknown to the server.</span></div><div class='line' id='LC156'><span class="cm"> * @property {number}  INVALID_MESSAGE_TYPE    - Client passed an unknown/unsupported MessageType.</span></div><div class='line' id='LC157'><span class="cm"> * @property {number}  WRONG_METHOD_NAME       - Unused.</span></div><div class='line' id='LC158'><span class="cm"> * @property {number}  BAD_SEQUENCE_ID         - Unused in Thrift RPC, used to flag proprietary sequence number errors.</span></div><div class='line' id='LC159'><span class="cm"> * @property {number}  MISSING_RESULT          - Raised by a server processor if a handler fails to supply the required return result.</span></div><div class='line' id='LC160'><span class="cm"> * @property {number}  INTERNAL_ERROR          - Something bad happened.</span></div><div class='line' id='LC161'><span class="cm"> * @property {number}  PROTOCOL_ERROR          - The protocol layer failed to serialize or deserialize data.</span></div><div class='line' id='LC162'><span class="cm"> * @property {number}  INVALID_TRANSFORM       - Unused.</span></div><div class='line' id='LC163'><span class="cm"> * @property {number}  INVALID_PROTOCOL        - The protocol (or version) is not supported.</span></div><div class='line' id='LC164'><span class="cm"> * @property {number}  UNSUPPORTED_CLIENT_TYPE - Unused.</span></div><div class='line' id='LC165'><span class="cm"> */</span></div><div class='line' id='LC166'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">TApplicationExceptionType</span> <span class="o">=</span> <span class="p">{</span></div><div class='line' id='LC167'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;UNKNOWN&#39;</span> <span class="o">:</span> <span class="mi">0</span><span class="p">,</span></div><div class='line' id='LC168'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;UNKNOWN_METHOD&#39;</span> <span class="o">:</span> <span class="mi">1</span><span class="p">,</span></div><div class='line' id='LC169'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;INVALID_MESSAGE_TYPE&#39;</span> <span class="o">:</span> <span class="mi">2</span><span class="p">,</span></div><div class='line' id='LC170'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;WRONG_METHOD_NAME&#39;</span> <span class="o">:</span> <span class="mi">3</span><span class="p">,</span></div><div class='line' id='LC171'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;BAD_SEQUENCE_ID&#39;</span> <span class="o">:</span> <span class="mi">4</span><span class="p">,</span></div><div class='line' id='LC172'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;MISSING_RESULT&#39;</span> <span class="o">:</span> <span class="mi">5</span><span class="p">,</span></div><div class='line' id='LC173'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;INTERNAL_ERROR&#39;</span> <span class="o">:</span> <span class="mi">6</span><span class="p">,</span></div><div class='line' id='LC174'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;PROTOCOL_ERROR&#39;</span> <span class="o">:</span> <span class="mi">7</span><span class="p">,</span></div><div class='line' id='LC175'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;INVALID_TRANSFORM&#39;</span> <span class="o">:</span> <span class="mi">8</span><span class="p">,</span></div><div class='line' id='LC176'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;INVALID_PROTOCOL&#39;</span> <span class="o">:</span> <span class="mi">9</span><span class="p">,</span></div><div class='line' id='LC177'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;UNSUPPORTED_CLIENT_TYPE&#39;</span> <span class="o">:</span> <span class="mi">10</span></div><div class='line' id='LC178'><span class="p">};</span></div><div class='line' id='LC179'><br/></div><div class='line' id='LC180'><span class="cm">/**</span></div><div class='line' id='LC181'><span class="cm"> * Initializes a Thrift TApplicationException instance.</span></div><div class='line' id='LC182'><span class="cm"> * @constructor</span></div><div class='line' id='LC183'><span class="cm"> * @augments Thrift.TException</span></div><div class='line' id='LC184'><span class="cm"> * @param {string} message - The TApplicationException message (distinct from the Error message).</span></div><div class='line' id='LC185'><span class="cm"> * @param {Thrift.TApplicationExceptionType} [code] - The TApplicationExceptionType code.</span></div><div class='line' id='LC186'><span class="cm"> * @classdesc TApplicationException is the exception class used to propagate exceptions from an RPC server back to a calling client.</span></div><div class='line' id='LC187'><span class="cm">*/</span></div><div class='line' id='LC188'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">TApplicationException</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">message</span><span class="p">,</span> <span class="nx">code</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC189'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">message</span> <span class="o">=</span> <span class="nx">message</span><span class="p">;</span></div><div class='line' id='LC190'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">code</span> <span class="o">=</span> <span class="k">typeof</span> <span class="nx">code</span> <span class="o">===</span> <span class="s2">&quot;number&quot;</span> <span class="o">?</span> <span class="nx">code</span> <span class="o">:</span> <span class="mi">0</span><span class="p">;</span></div><div class='line' id='LC191'><span class="p">};</span></div><div class='line' id='LC192'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">inherits</span><span class="p">(</span><span class="nx">Thrift</span><span class="p">.</span><span class="nx">TApplicationException</span><span class="p">,</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">TException</span><span class="p">,</span> <span class="s1">&#39;TApplicationException&#39;</span><span class="p">);</span></div><div class='line' id='LC193'><br/></div><div class='line' id='LC194'><span class="cm">/**</span></div><div class='line' id='LC195'><span class="cm"> * Read a TApplicationException from the supplied protocol.</span></div><div class='line' id='LC196'><span class="cm"> * @param {object} input - The input protocol to read from.</span></div><div class='line' id='LC197'><span class="cm"> */</span></div><div class='line' id='LC198'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">TApplicationException</span><span class="p">.</span><span class="nx">prototype</span><span class="p">.</span><span class="nx">read</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">input</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC199'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">while</span> <span class="p">(</span><span class="mi">1</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC200'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">ret</span> <span class="o">=</span> <span class="nx">input</span><span class="p">.</span><span class="nx">readFieldBegin</span><span class="p">();</span></div><div class='line' id='LC201'><br/></div><div class='line' id='LC202'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">ret</span><span class="p">.</span><span class="nx">ftype</span> <span class="o">==</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">STOP</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC203'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">break</span><span class="p">;</span></div><div class='line' id='LC204'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC205'><br/></div><div class='line' id='LC206'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">fid</span> <span class="o">=</span> <span class="nx">ret</span><span class="p">.</span><span class="nx">fid</span><span class="p">;</span></div><div class='line' id='LC207'><br/></div><div class='line' id='LC208'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">switch</span> <span class="p">(</span><span class="nx">fid</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC209'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">case</span> <span class="mi">1</span><span class="o">:</span></div><div class='line' id='LC210'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">ret</span><span class="p">.</span><span class="nx">ftype</span> <span class="o">==</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">STRING</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC211'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">ret</span> <span class="o">=</span> <span class="nx">input</span><span class="p">.</span><span class="nx">readString</span><span class="p">();</span></div><div class='line' id='LC212'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">message</span> <span class="o">=</span> <span class="nx">ret</span><span class="p">.</span><span class="nx">value</span><span class="p">;</span></div><div class='line' id='LC213'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span> <span class="k">else</span> <span class="p">{</span></div><div class='line' id='LC214'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">ret</span> <span class="o">=</span> <span class="nx">input</span><span class="p">.</span><span class="nx">skip</span><span class="p">(</span><span class="nx">ret</span><span class="p">.</span><span class="nx">ftype</span><span class="p">);</span></div><div class='line' id='LC215'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC216'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">break</span><span class="p">;</span></div><div class='line' id='LC217'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">case</span> <span class="mi">2</span><span class="o">:</span></div><div class='line' id='LC218'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">ret</span><span class="p">.</span><span class="nx">ftype</span> <span class="o">==</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">I32</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC219'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">ret</span> <span class="o">=</span> <span class="nx">input</span><span class="p">.</span><span class="nx">readI32</span><span class="p">();</span></div><div class='line' id='LC220'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">code</span> <span class="o">=</span> <span class="nx">ret</span><span class="p">.</span><span class="nx">value</span><span class="p">;</span></div><div class='line' id='LC221'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span> <span class="k">else</span> <span class="p">{</span></div><div class='line' id='LC222'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">ret</span> <span class="o">=</span> <span class="nx">input</span><span class="p">.</span><span class="nx">skip</span><span class="p">(</span><span class="nx">ret</span><span class="p">.</span><span class="nx">ftype</span><span class="p">);</span></div><div class='line' id='LC223'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC224'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">break</span><span class="p">;</span></div><div class='line' id='LC225'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">default</span><span class="o">:</span></div><div class='line' id='LC226'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">ret</span> <span class="o">=</span> <span class="nx">input</span><span class="p">.</span><span class="nx">skip</span><span class="p">(</span><span class="nx">ret</span><span class="p">.</span><span class="nx">ftype</span><span class="p">);</span></div><div class='line' id='LC227'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">break</span><span class="p">;</span></div><div class='line' id='LC228'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC229'><br/></div><div class='line' id='LC230'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">input</span><span class="p">.</span><span class="nx">readFieldEnd</span><span class="p">();</span></div><div class='line' id='LC231'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC232'><br/></div><div class='line' id='LC233'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">input</span><span class="p">.</span><span class="nx">readStructEnd</span><span class="p">();</span></div><div class='line' id='LC234'><span class="p">};</span></div><div class='line' id='LC235'><br/></div><div class='line' id='LC236'><span class="cm">/**</span></div><div class='line' id='LC237'><span class="cm"> * Wite a TApplicationException to the supplied protocol.</span></div><div class='line' id='LC238'><span class="cm"> * @param {object} output - The output protocol to write to.</span></div><div class='line' id='LC239'><span class="cm"> */</span></div><div class='line' id='LC240'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">TApplicationException</span><span class="p">.</span><span class="nx">prototype</span><span class="p">.</span><span class="nx">write</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">output</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC241'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">output</span><span class="p">.</span><span class="nx">writeStructBegin</span><span class="p">(</span><span class="s1">&#39;TApplicationException&#39;</span><span class="p">);</span></div><div class='line' id='LC242'><br/></div><div class='line' id='LC243'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">message</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC244'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">output</span><span class="p">.</span><span class="nx">writeFieldBegin</span><span class="p">(</span><span class="s1">&#39;message&#39;</span><span class="p">,</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">STRING</span><span class="p">,</span> <span class="mi">1</span><span class="p">);</span></div><div class='line' id='LC245'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">output</span><span class="p">.</span><span class="nx">writeString</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">getMessage</span><span class="p">());</span></div><div class='line' id='LC246'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">output</span><span class="p">.</span><span class="nx">writeFieldEnd</span><span class="p">();</span></div><div class='line' id='LC247'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC248'><br/></div><div class='line' id='LC249'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">code</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC250'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">output</span><span class="p">.</span><span class="nx">writeFieldBegin</span><span class="p">(</span><span class="s1">&#39;type&#39;</span><span class="p">,</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">I32</span><span class="p">,</span> <span class="mi">2</span><span class="p">);</span></div><div class='line' id='LC251'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">output</span><span class="p">.</span><span class="nx">writeI32</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">code</span><span class="p">);</span></div><div class='line' id='LC252'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">output</span><span class="p">.</span><span class="nx">writeFieldEnd</span><span class="p">();</span></div><div class='line' id='LC253'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC254'><br/></div><div class='line' id='LC255'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">output</span><span class="p">.</span><span class="nx">writeFieldStop</span><span class="p">();</span></div><div class='line' id='LC256'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">output</span><span class="p">.</span><span class="nx">writeStructEnd</span><span class="p">();</span></div><div class='line' id='LC257'><span class="p">};</span></div><div class='line' id='LC258'><br/></div><div class='line' id='LC259'><span class="cm">/**</span></div><div class='line' id='LC260'><span class="cm"> * Returns the application exception code set on the exception.</span></div><div class='line' id='LC261'><span class="cm"> * @readonly</span></div><div class='line' id='LC262'><span class="cm"> * @returns {Thrift.TApplicationExceptionType} exception code</span></div><div class='line' id='LC263'><span class="cm"> */</span></div><div class='line' id='LC264'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">TApplicationException</span><span class="p">.</span><span class="nx">prototype</span><span class="p">.</span><span class="nx">getCode</span> <span class="o">=</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC265'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="k">this</span><span class="p">.</span><span class="nx">code</span><span class="p">;</span></div><div class='line' id='LC266'><span class="p">};</span></div><div class='line' id='LC267'><br/></div><div class='line' id='LC268'><span class="cm">/**</span></div><div class='line' id='LC269'><span class="cm"> * Initializes a Thrift Http[s] transport instance.</span></div><div class='line' id='LC270'><span class="cm"> * Note: If you do not specify a url then you must handle XHR on your own</span></div><div class='line' id='LC271'><span class="cm"> *       (this is how to use js bindings in a async fashion).</span></div><div class='line' id='LC272'><span class="cm"> * @constructor</span></div><div class='line' id='LC273'><span class="cm"> * @param {string} [url] - The URL to connect to.</span></div><div class='line' id='LC274'><span class="cm"> * @classdesc The Apache Thrift Transport layer performs byte level I/O between RPC</span></div><div class='line' id='LC275'><span class="cm"> * clients and servers. The JavaScript Transport object type uses Http[s]/XHR and is</span></div><div class='line' id='LC276'><span class="cm"> * the sole browser based Thrift transport. Target servers must implement the http[s] </span></div><div class='line' id='LC277'><span class="cm"> * transport (see: node.js example server).</span></div><div class='line' id='LC278'><span class="cm"> * @example</span></div><div class='line' id='LC279'><span class="cm"> *     var transport = new Thrift.Transport(&quot;http://localhost:8585&quot;);</span></div><div class='line' id='LC280'><span class="cm"> */</span></div><div class='line' id='LC281'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Transport</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">url</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC282'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">url</span> <span class="o">=</span> <span class="nx">url</span><span class="p">;</span></div><div class='line' id='LC283'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">wpos</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span></div><div class='line' id='LC284'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rpos</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span></div><div class='line' id='LC285'><br/></div><div class='line' id='LC286'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">send_buf</span> <span class="o">=</span> <span class="s1">&#39;&#39;</span><span class="p">;</span></div><div class='line' id='LC287'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">recv_buf</span> <span class="o">=</span> <span class="s1">&#39;&#39;</span><span class="p">;</span></div><div class='line' id='LC288'><span class="p">};</span></div><div class='line' id='LC289'><br/></div><div class='line' id='LC290'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Transport</span><span class="p">.</span><span class="nx">prototype</span> <span class="o">=</span> <span class="p">{</span></div><div class='line' id='LC291'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC292'><span class="cm">     * Gets the browser specific XmlHttpRequest Object.</span></div><div class='line' id='LC293'><span class="cm">     * @returns {object} the browser XHR interface object</span></div><div class='line' id='LC294'><span class="cm">     */</span></div><div class='line' id='LC295'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">getXmlHttpRequestObject</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC296'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">try</span> <span class="p">{</span> <span class="k">return</span> <span class="k">new</span> <span class="nx">XMLHttpRequest</span><span class="p">();</span> <span class="p">}</span> <span class="k">catch</span> <span class="p">(</span><span class="nx">e1</span><span class="p">)</span> <span class="p">{</span> <span class="p">}</span></div><div class='line' id='LC297'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">try</span> <span class="p">{</span> <span class="k">return</span> <span class="k">new</span> <span class="nx">ActiveXObject</span><span class="p">(</span><span class="s1">&#39;Msxml2.XMLHTTP&#39;</span><span class="p">);</span> <span class="p">}</span> <span class="k">catch</span> <span class="p">(</span><span class="nx">e2</span><span class="p">)</span> <span class="p">{</span> <span class="p">}</span></div><div class='line' id='LC298'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">try</span> <span class="p">{</span> <span class="k">return</span> <span class="k">new</span> <span class="nx">ActiveXObject</span><span class="p">(</span><span class="s1">&#39;Microsoft.XMLHTTP&#39;</span><span class="p">);</span> <span class="p">}</span> <span class="k">catch</span> <span class="p">(</span><span class="nx">e3</span><span class="p">)</span> <span class="p">{</span> <span class="p">}</span></div><div class='line' id='LC299'><br/></div><div class='line' id='LC300'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">throw</span> <span class="s2">&quot;Your browser doesn&#39;t support XHR.&quot;</span><span class="p">;</span></div><div class='line' id='LC301'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC302'><br/></div><div class='line' id='LC303'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC304'><span class="cm">     * Sends the current XRH request if the transport was created with a URL and</span></div><div class='line' id='LC305'><span class="cm">     * the async parameter if false. If the transport was not created with a URL</span></div><div class='line' id='LC306'><span class="cm">     * or the async parameter is True or the URL is an empty string, the current </span></div><div class='line' id='LC307'><span class="cm">     * send buffer is returned.</span></div><div class='line' id='LC308'><span class="cm">     * @param {object} async - If true the current send buffer is returned.</span></div><div class='line' id='LC309'><span class="cm">     * @returns {undefined|string} Nothing or the current send buffer.</span></div><div class='line' id='LC310'><span class="cm">     * @throws {string} If XHR fails.</span></div><div class='line' id='LC311'><span class="cm">     */</span></div><div class='line' id='LC312'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">flush</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">async</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC313'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="c1">//async mode</span></div><div class='line' id='LC314'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">async</span> <span class="o">||</span> <span class="k">this</span><span class="p">.</span><span class="nx">url</span> <span class="o">===</span> <span class="kc">undefined</span> <span class="o">||</span> <span class="k">this</span><span class="p">.</span><span class="nx">url</span> <span class="o">===</span> <span class="s1">&#39;&#39;</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC315'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="k">this</span><span class="p">.</span><span class="nx">send_buf</span><span class="p">;</span></div><div class='line' id='LC316'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC317'><br/></div><div class='line' id='LC318'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">xreq</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">getXmlHttpRequestObject</span><span class="p">();</span></div><div class='line' id='LC319'><br/></div><div class='line' id='LC320'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">xreq</span><span class="p">.</span><span class="nx">overrideMimeType</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC321'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">xreq</span><span class="p">.</span><span class="nx">overrideMimeType</span><span class="p">(</span><span class="s1">&#39;application/json&#39;</span><span class="p">);</span></div><div class='line' id='LC322'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC323'><br/></div><div class='line' id='LC324'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">xreq</span><span class="p">.</span><span class="nx">open</span><span class="p">(</span><span class="s1">&#39;POST&#39;</span><span class="p">,</span> <span class="k">this</span><span class="p">.</span><span class="nx">url</span><span class="p">,</span> <span class="kc">false</span><span class="p">);</span></div><div class='line' id='LC325'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">xreq</span><span class="p">.</span><span class="nx">send</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">send_buf</span><span class="p">);</span></div><div class='line' id='LC326'><br/></div><div class='line' id='LC327'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">xreq</span><span class="p">.</span><span class="nx">readyState</span> <span class="o">!=</span> <span class="mi">4</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC328'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">throw</span> <span class="s1">&#39;encountered an unknown ajax ready state: &#39;</span> <span class="o">+</span> <span class="nx">xreq</span><span class="p">.</span><span class="nx">readyState</span><span class="p">;</span></div><div class='line' id='LC329'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC330'><br/></div><div class='line' id='LC331'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">xreq</span><span class="p">.</span><span class="nx">status</span> <span class="o">!=</span> <span class="mi">200</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC332'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">throw</span> <span class="s1">&#39;encountered a unknown request status: &#39;</span> <span class="o">+</span> <span class="nx">xreq</span><span class="p">.</span><span class="nx">status</span><span class="p">;</span></div><div class='line' id='LC333'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC334'><br/></div><div class='line' id='LC335'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">recv_buf</span> <span class="o">=</span> <span class="nx">xreq</span><span class="p">.</span><span class="nx">responseText</span><span class="p">;</span></div><div class='line' id='LC336'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">recv_buf_sz</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">recv_buf</span><span class="p">.</span><span class="nx">length</span><span class="p">;</span></div><div class='line' id='LC337'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">wpos</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">recv_buf</span><span class="p">.</span><span class="nx">length</span><span class="p">;</span></div><div class='line' id='LC338'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rpos</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span></div><div class='line' id='LC339'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC340'><br/></div><div class='line' id='LC341'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC342'><span class="cm">     * Creates a jQuery XHR object to be used for a Thrift server call.</span></div><div class='line' id='LC343'><span class="cm">     * @param {object} client - The Thrift Service client object generated by the IDL compiler.</span></div><div class='line' id='LC344'><span class="cm">     * @param {object} postData - The message to send to the server.</span></div><div class='line' id='LC345'><span class="cm">     * @param {function} args - The function to call if the request suceeds.</span></div><div class='line' id='LC346'><span class="cm">     * @param {function} recv_method - The Thrift Service Client receive method for the call.</span></div><div class='line' id='LC347'><span class="cm">     * @returns {object} A new jQuery XHR object.</span></div><div class='line' id='LC348'><span class="cm">     * @throws {string} If the jQuery version is prior to 1.5 or if jQuery is not found.</span></div><div class='line' id='LC349'><span class="cm">     */</span></div><div class='line' id='LC350'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">jqRequest</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">client</span><span class="p">,</span> <span class="nx">postData</span><span class="p">,</span> <span class="nx">args</span><span class="p">,</span> <span class="nx">recv_method</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC351'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="k">typeof</span> <span class="nx">jQuery</span> <span class="o">===</span> <span class="s1">&#39;undefined&#39;</span> <span class="o">||</span></div><div class='line' id='LC352'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">typeof</span> <span class="nx">jQuery</span><span class="p">.</span><span class="nx">Deferred</span> <span class="o">===</span> <span class="s1">&#39;undefined&#39;</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC353'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">throw</span> <span class="s1">&#39;Thrift.js requires jQuery 1.5+ to use asynchronous requests&#39;</span><span class="p">;</span></div><div class='line' id='LC354'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC355'><br/></div><div class='line' id='LC356'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">thriftTransport</span> <span class="o">=</span> <span class="k">this</span><span class="p">;</span></div><div class='line' id='LC357'><br/></div><div class='line' id='LC358'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">jqXHR</span> <span class="o">=</span> <span class="nx">jQuery</span><span class="p">.</span><span class="nx">ajax</span><span class="p">({</span></div><div class='line' id='LC359'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">url</span><span class="o">:</span> <span class="k">this</span><span class="p">.</span><span class="nx">url</span><span class="p">,</span></div><div class='line' id='LC360'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">data</span><span class="o">:</span> <span class="nx">postData</span><span class="p">,</span></div><div class='line' id='LC361'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">type</span><span class="o">:</span> <span class="s1">&#39;POST&#39;</span><span class="p">,</span></div><div class='line' id='LC362'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">cache</span><span class="o">:</span> <span class="kc">false</span><span class="p">,</span></div><div class='line' id='LC363'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">contentType</span><span class="o">:</span> <span class="s1">&#39;application/json&#39;</span><span class="p">,</span></div><div class='line' id='LC364'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">dataType</span><span class="o">:</span> <span class="s1">&#39;text thrift&#39;</span><span class="p">,</span></div><div class='line' id='LC365'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">converters</span><span class="o">:</span> <span class="p">{</span></div><div class='line' id='LC366'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s1">&#39;text thrift&#39;</span> <span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">responseData</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC367'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">thriftTransport</span><span class="p">.</span><span class="nx">setRecvBuffer</span><span class="p">(</span><span class="nx">responseData</span><span class="p">);</span></div><div class='line' id='LC368'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">value</span> <span class="o">=</span> <span class="nx">recv_method</span><span class="p">.</span><span class="nx">call</span><span class="p">(</span><span class="nx">client</span><span class="p">);</span></div><div class='line' id='LC369'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nx">value</span><span class="p">;</span></div><div class='line' id='LC370'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC371'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC372'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">context</span><span class="o">:</span> <span class="nx">client</span><span class="p">,</span></div><div class='line' id='LC373'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">success</span><span class="o">:</span> <span class="nx">jQuery</span><span class="p">.</span><span class="nx">makeArray</span><span class="p">(</span><span class="nx">args</span><span class="p">).</span><span class="nx">pop</span><span class="p">()</span></div><div class='line' id='LC374'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">});</span></div><div class='line' id='LC375'><br/></div><div class='line' id='LC376'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nx">jqXHR</span><span class="p">;</span></div><div class='line' id='LC377'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC378'><br/></div><div class='line' id='LC379'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC380'><span class="cm">     * Sets the buffer to use when receiving server responses.</span></div><div class='line' id='LC381'><span class="cm">     * @param {string} buf - The buffer to receive server responses.</span></div><div class='line' id='LC382'><span class="cm">     */</span></div><div class='line' id='LC383'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">setRecvBuffer</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">buf</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC384'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">recv_buf</span> <span class="o">=</span> <span class="nx">buf</span><span class="p">;</span></div><div class='line' id='LC385'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">recv_buf_sz</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">recv_buf</span><span class="p">.</span><span class="nx">length</span><span class="p">;</span></div><div class='line' id='LC386'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">wpos</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">recv_buf</span><span class="p">.</span><span class="nx">length</span><span class="p">;</span></div><div class='line' id='LC387'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rpos</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span></div><div class='line' id='LC388'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC389'><br/></div><div class='line' id='LC390'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC391'><span class="cm">     * Returns true if the transport is open, in browser based JavaScript</span></div><div class='line' id='LC392'><span class="cm">     * this function always returns true.</span></div><div class='line' id='LC393'><span class="cm">     * @readonly</span></div><div class='line' id='LC394'><span class="cm">     * @returns {boolean} Always True.</span></div><div class='line' id='LC395'><span class="cm">     */</span>    </div><div class='line' id='LC396'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">isOpen</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC397'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="kc">true</span><span class="p">;</span></div><div class='line' id='LC398'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC399'><br/></div><div class='line' id='LC400'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC401'><span class="cm">     * Opens the transport connection, in browser based JavaScript</span></div><div class='line' id='LC402'><span class="cm">     * this function is a nop.</span></div><div class='line' id='LC403'><span class="cm">     */</span>    </div><div class='line' id='LC404'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">open</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{},</span></div><div class='line' id='LC405'><br/></div><div class='line' id='LC406'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC407'><span class="cm">     * Closes the transport connection, in browser based JavaScript</span></div><div class='line' id='LC408'><span class="cm">     * this function is a nop.</span></div><div class='line' id='LC409'><span class="cm">     */</span>    </div><div class='line' id='LC410'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">close</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{},</span></div><div class='line' id='LC411'><br/></div><div class='line' id='LC412'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC413'><span class="cm">     * Returns the specified number of characters from the response</span></div><div class='line' id='LC414'><span class="cm">     * buffer.</span></div><div class='line' id='LC415'><span class="cm">     * @param {number} len - The number of characters to return.</span></div><div class='line' id='LC416'><span class="cm">     * @returns {string} Characters sent by the server.</span></div><div class='line' id='LC417'><span class="cm">     */</span></div><div class='line' id='LC418'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">read</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">len</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC419'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">avail</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">wpos</span> <span class="o">-</span> <span class="k">this</span><span class="p">.</span><span class="nx">rpos</span><span class="p">;</span></div><div class='line' id='LC420'><br/></div><div class='line' id='LC421'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">avail</span> <span class="o">===</span> <span class="mi">0</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC422'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="s1">&#39;&#39;</span><span class="p">;</span></div><div class='line' id='LC423'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC424'><br/></div><div class='line' id='LC425'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">give</span> <span class="o">=</span> <span class="nx">len</span><span class="p">;</span></div><div class='line' id='LC426'><br/></div><div class='line' id='LC427'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">avail</span> <span class="o">&lt;</span> <span class="nx">len</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC428'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">give</span> <span class="o">=</span> <span class="nx">avail</span><span class="p">;</span></div><div class='line' id='LC429'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC430'><br/></div><div class='line' id='LC431'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">ret</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">read_buf</span><span class="p">.</span><span class="nx">substr</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">rpos</span><span class="p">,</span> <span class="nx">give</span><span class="p">);</span></div><div class='line' id='LC432'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rpos</span> <span class="o">+=</span> <span class="nx">give</span><span class="p">;</span></div><div class='line' id='LC433'><br/></div><div class='line' id='LC434'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="c1">//clear buf when complete?</span></div><div class='line' id='LC435'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nx">ret</span><span class="p">;</span></div><div class='line' id='LC436'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC437'><br/></div><div class='line' id='LC438'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC439'><span class="cm">     * Returns the entire response buffer.</span></div><div class='line' id='LC440'><span class="cm">     * @returns {string} Characters sent by the server.</span></div><div class='line' id='LC441'><span class="cm">     */</span></div><div class='line' id='LC442'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readAll</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC443'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="k">this</span><span class="p">.</span><span class="nx">recv_buf</span><span class="p">;</span></div><div class='line' id='LC444'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC445'><br/></div><div class='line' id='LC446'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC447'><span class="cm">     * Sets the send buffer to buf.</span></div><div class='line' id='LC448'><span class="cm">     * @param {string} buf - The buffer to send.</span></div><div class='line' id='LC449'><span class="cm">     */</span>    </div><div class='line' id='LC450'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">write</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">buf</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC451'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">send_buf</span> <span class="o">=</span> <span class="nx">buf</span><span class="p">;</span></div><div class='line' id='LC452'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC453'><br/></div><div class='line' id='LC454'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC455'><span class="cm">     * Returns the send buffer.</span></div><div class='line' id='LC456'><span class="cm">     * @readonly</span></div><div class='line' id='LC457'><span class="cm">     * @returns {string} The send buffer.</span></div><div class='line' id='LC458'><span class="cm">     */</span> </div><div class='line' id='LC459'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">getSendBuffer</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC460'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="k">this</span><span class="p">.</span><span class="nx">send_buf</span><span class="p">;</span></div><div class='line' id='LC461'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC462'><br/></div><div class='line' id='LC463'><span class="p">};</span></div><div class='line' id='LC464'><br/></div><div class='line' id='LC465'><span class="cm">/**</span></div><div class='line' id='LC466'><span class="cm"> * Initializes a Thrift JSON protocol instance.</span></div><div class='line' id='LC467'><span class="cm"> * @constructor</span></div><div class='line' id='LC468'><span class="cm"> * @param {Thrift.Transport} transport - The transport to serialize to/from.</span></div><div class='line' id='LC469'><span class="cm"> * @classdesc Apache Thrift Protocols perform serialization which enables cross </span></div><div class='line' id='LC470'><span class="cm"> * language RPC. The Protocol type is the JavaScript browser implementation </span></div><div class='line' id='LC471'><span class="cm"> * of the Apache Thrift TJSONProtocol.</span></div><div class='line' id='LC472'><span class="cm"> * @example</span></div><div class='line' id='LC473'><span class="cm"> *     var protocol  = new Thrift.Protocol(transport);</span></div><div class='line' id='LC474'><span class="cm"> */</span></div><div class='line' id='LC475'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">transport</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC476'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">transport</span> <span class="o">=</span> <span class="nx">transport</span><span class="p">;</span></div><div class='line' id='LC477'><span class="p">};</span></div><div class='line' id='LC478'><br/></div><div class='line' id='LC479'><span class="cm">/**</span></div><div class='line' id='LC480'><span class="cm"> * Thrift IDL type Id to string mapping.</span></div><div class='line' id='LC481'><span class="cm"> * @readonly</span></div><div class='line' id='LC482'><span class="cm"> * @see {@link Thrift.Type}</span></div><div class='line' id='LC483'><span class="cm"> */</span></div><div class='line' id='LC484'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Type</span> <span class="o">=</span> <span class="p">{};</span></div><div class='line' id='LC485'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Type</span><span class="p">[</span><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">BOOL</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;&quot;tf&quot;&#39;</span><span class="p">;</span></div><div class='line' id='LC486'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Type</span><span class="p">[</span><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">BYTE</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;&quot;i8&quot;&#39;</span><span class="p">;</span></div><div class='line' id='LC487'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Type</span><span class="p">[</span><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">I16</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;&quot;i16&quot;&#39;</span><span class="p">;</span></div><div class='line' id='LC488'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Type</span><span class="p">[</span><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">I32</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;&quot;i32&quot;&#39;</span><span class="p">;</span></div><div class='line' id='LC489'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Type</span><span class="p">[</span><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">I64</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;&quot;i64&quot;&#39;</span><span class="p">;</span></div><div class='line' id='LC490'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Type</span><span class="p">[</span><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">DOUBLE</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;&quot;dbl&quot;&#39;</span><span class="p">;</span></div><div class='line' id='LC491'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Type</span><span class="p">[</span><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">STRUCT</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;&quot;rec&quot;&#39;</span><span class="p">;</span></div><div class='line' id='LC492'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Type</span><span class="p">[</span><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">STRING</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;&quot;str&quot;&#39;</span><span class="p">;</span></div><div class='line' id='LC493'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Type</span><span class="p">[</span><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">MAP</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;&quot;map&quot;&#39;</span><span class="p">;</span></div><div class='line' id='LC494'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Type</span><span class="p">[</span><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">LIST</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;&quot;lst&quot;&#39;</span><span class="p">;</span></div><div class='line' id='LC495'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Type</span><span class="p">[</span><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">SET</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;&quot;set&quot;&#39;</span><span class="p">;</span></div><div class='line' id='LC496'><br/></div><div class='line' id='LC497'><span class="cm">/**</span></div><div class='line' id='LC498'><span class="cm"> * Thrift IDL type string to Id mapping.</span></div><div class='line' id='LC499'><span class="cm"> * @readonly</span></div><div class='line' id='LC500'><span class="cm"> * @see {@link Thrift.Type}</span></div><div class='line' id='LC501'><span class="cm"> */</span></div><div class='line' id='LC502'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">RType</span> <span class="o">=</span> <span class="p">{};</span></div><div class='line' id='LC503'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">RType</span><span class="p">.</span><span class="nx">tf</span> <span class="o">=</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">BOOL</span><span class="p">;</span></div><div class='line' id='LC504'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">RType</span><span class="p">.</span><span class="nx">i8</span> <span class="o">=</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">BYTE</span><span class="p">;</span></div><div class='line' id='LC505'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">RType</span><span class="p">.</span><span class="nx">i16</span> <span class="o">=</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">I16</span><span class="p">;</span></div><div class='line' id='LC506'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">RType</span><span class="p">.</span><span class="nx">i32</span> <span class="o">=</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">I32</span><span class="p">;</span></div><div class='line' id='LC507'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">RType</span><span class="p">.</span><span class="nx">i64</span> <span class="o">=</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">I64</span><span class="p">;</span></div><div class='line' id='LC508'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">RType</span><span class="p">.</span><span class="nx">dbl</span> <span class="o">=</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">DOUBLE</span><span class="p">;</span></div><div class='line' id='LC509'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">RType</span><span class="p">.</span><span class="nx">rec</span> <span class="o">=</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">STRUCT</span><span class="p">;</span></div><div class='line' id='LC510'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">RType</span><span class="p">.</span><span class="nx">str</span> <span class="o">=</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">STRING</span><span class="p">;</span></div><div class='line' id='LC511'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">RType</span><span class="p">.</span><span class="nx">map</span> <span class="o">=</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">MAP</span><span class="p">;</span></div><div class='line' id='LC512'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">RType</span><span class="p">.</span><span class="nx">lst</span> <span class="o">=</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">LIST</span><span class="p">;</span></div><div class='line' id='LC513'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">RType</span><span class="p">.</span><span class="nx">set</span> <span class="o">=</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">SET</span><span class="p">;</span></div><div class='line' id='LC514'><br/></div><div class='line' id='LC515'><span class="cm">/**</span></div><div class='line' id='LC516'><span class="cm"> * The TJSONProtocol version number.</span></div><div class='line' id='LC517'><span class="cm"> * @readonly</span></div><div class='line' id='LC518'><span class="cm"> * @const {number} Version</span></div><div class='line' id='LC519'><span class="cm"> * @memberof Thrift.Protocol</span></div><div class='line' id='LC520'><span class="cm"> */</span></div><div class='line' id='LC521'>&nbsp;<span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Version</span> <span class="o">=</span> <span class="mi">1</span><span class="p">;</span></div><div class='line' id='LC522'><br/></div><div class='line' id='LC523'><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">prototype</span> <span class="o">=</span> <span class="p">{</span></div><div class='line' id='LC524'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC525'><span class="cm">     * Returns the underlying transport.</span></div><div class='line' id='LC526'><span class="cm">     * @readonly</span></div><div class='line' id='LC527'><span class="cm">     * @returns {Thrift.Transport} The underlying transport.</span></div><div class='line' id='LC528'><span class="cm">     */</span> </div><div class='line' id='LC529'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">getTransport</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC530'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="k">this</span><span class="p">.</span><span class="nx">transport</span><span class="p">;</span></div><div class='line' id='LC531'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC532'><br/></div><div class='line' id='LC533'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC534'><span class="cm">     * Serializes the beginning of a Thrift RPC message.</span></div><div class='line' id='LC535'><span class="cm">     * @param {string} name - The service method to call.</span></div><div class='line' id='LC536'><span class="cm">     * @param {Thrift.MessageType} messageType - The type of method call.</span></div><div class='line' id='LC537'><span class="cm">     * @param {number} seqid - The sequence number of this call (always 0 in Apache Thrift).</span></div><div class='line' id='LC538'><span class="cm">     */</span></div><div class='line' id='LC539'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeMessageBegin</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">name</span><span class="p">,</span> <span class="nx">messageType</span><span class="p">,</span> <span class="nx">seqid</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC540'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span> <span class="o">=</span> <span class="p">[];</span></div><div class='line' id='LC541'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tpos</span> <span class="o">=</span> <span class="p">[];</span></div><div class='line' id='LC542'><br/></div><div class='line' id='LC543'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">push</span><span class="p">([</span><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Version</span><span class="p">,</span> <span class="s1">&#39;&quot;&#39;</span> <span class="o">+</span></div><div class='line' id='LC544'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">name</span> <span class="o">+</span> <span class="s1">&#39;&quot;&#39;</span><span class="p">,</span> <span class="nx">messageType</span><span class="p">,</span> <span class="nx">seqid</span><span class="p">]);</span></div><div class='line' id='LC545'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC546'><br/></div><div class='line' id='LC547'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC548'><span class="cm">     * Serializes the end of a Thrift RPC message.</span></div><div class='line' id='LC549'><span class="cm">     */</span></div><div class='line' id='LC550'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeMessageEnd</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC551'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">obj</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">pop</span><span class="p">();</span></div><div class='line' id='LC552'><br/></div><div class='line' id='LC553'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">wobj</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">pop</span><span class="p">();</span></div><div class='line' id='LC554'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">wobj</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="nx">obj</span><span class="p">);</span></div><div class='line' id='LC555'><br/></div><div class='line' id='LC556'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">wbuf</span> <span class="o">=</span> <span class="s1">&#39;[&#39;</span> <span class="o">+</span> <span class="k">this</span><span class="p">.</span><span class="nx">wobj</span><span class="p">.</span><span class="nx">join</span><span class="p">(</span><span class="s1">&#39;,&#39;</span><span class="p">)</span> <span class="o">+</span> <span class="s1">&#39;]&#39;</span><span class="p">;</span></div><div class='line' id='LC557'><br/></div><div class='line' id='LC558'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">transport</span><span class="p">.</span><span class="nx">write</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">wbuf</span><span class="p">);</span></div><div class='line' id='LC559'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC560'><br/></div><div class='line' id='LC561'><br/></div><div class='line' id='LC562'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC563'><span class="cm">     * Serializes the beginning of a struct.</span></div><div class='line' id='LC564'><span class="cm">     * @param {string} name - The name of the struct.</span></div><div class='line' id='LC565'><span class="cm">     */</span></div><div class='line' id='LC566'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeStructBegin</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">name</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC567'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tpos</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">length</span><span class="p">);</span></div><div class='line' id='LC568'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">push</span><span class="p">({});</span></div><div class='line' id='LC569'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC570'><br/></div><div class='line' id='LC571'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC572'><span class="cm">     * Serializes the end of a struct.</span></div><div class='line' id='LC573'><span class="cm">     */</span></div><div class='line' id='LC574'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeStructEnd</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC575'><br/></div><div class='line' id='LC576'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">p</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">tpos</span><span class="p">.</span><span class="nx">pop</span><span class="p">();</span></div><div class='line' id='LC577'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">struct</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">[</span><span class="nx">p</span><span class="p">];</span></div><div class='line' id='LC578'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">str</span> <span class="o">=</span> <span class="s1">&#39;{&#39;</span><span class="p">;</span></div><div class='line' id='LC579'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">first</span> <span class="o">=</span> <span class="kc">true</span><span class="p">;</span></div><div class='line' id='LC580'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">for</span> <span class="p">(</span><span class="kd">var</span> <span class="nx">key</span> <span class="k">in</span> <span class="nx">struct</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC581'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">first</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC582'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">first</span> <span class="o">=</span> <span class="kc">false</span><span class="p">;</span></div><div class='line' id='LC583'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span> <span class="k">else</span> <span class="p">{</span></div><div class='line' id='LC584'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">str</span> <span class="o">+=</span> <span class="s1">&#39;,&#39;</span><span class="p">;</span></div><div class='line' id='LC585'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC586'><br/></div><div class='line' id='LC587'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">str</span> <span class="o">+=</span> <span class="nx">key</span> <span class="o">+</span> <span class="s1">&#39;:&#39;</span> <span class="o">+</span> <span class="nx">struct</span><span class="p">[</span><span class="nx">key</span><span class="p">];</span></div><div class='line' id='LC588'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC589'><br/></div><div class='line' id='LC590'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">str</span> <span class="o">+=</span> <span class="s1">&#39;}&#39;</span><span class="p">;</span></div><div class='line' id='LC591'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">[</span><span class="nx">p</span><span class="p">]</span> <span class="o">=</span> <span class="nx">str</span><span class="p">;</span></div><div class='line' id='LC592'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC593'><br/></div><div class='line' id='LC594'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC595'><span class="cm">     * Serializes the beginning of a struct field.</span></div><div class='line' id='LC596'><span class="cm">     * @param {string} name - The name of the field.</span></div><div class='line' id='LC597'><span class="cm">     * @param {Thrift.Protocol.Type} fieldType - The data type of the field.</span></div><div class='line' id='LC598'><span class="cm">     * @param {number} fieldId - The field&#39;s unique identifier.</span></div><div class='line' id='LC599'><span class="cm">     */</span></div><div class='line' id='LC600'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeFieldBegin</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">name</span><span class="p">,</span> <span class="nx">fieldType</span><span class="p">,</span> <span class="nx">fieldId</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC601'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tpos</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">length</span><span class="p">);</span></div><div class='line' id='LC602'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">push</span><span class="p">({</span> <span class="s1">&#39;fieldId&#39;</span><span class="o">:</span> <span class="s1">&#39;&quot;&#39;</span> <span class="o">+</span></div><div class='line' id='LC603'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">fieldId</span> <span class="o">+</span> <span class="s1">&#39;&quot;&#39;</span><span class="p">,</span> <span class="s1">&#39;fieldType&#39;</span><span class="o">:</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Type</span><span class="p">[</span><span class="nx">fieldType</span><span class="p">]</span></div><div class='line' id='LC604'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">});</span></div><div class='line' id='LC605'><br/></div><div class='line' id='LC606'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC607'><br/></div><div class='line' id='LC608'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC609'><span class="cm">     * Serializes the end of a field.</span></div><div class='line' id='LC610'><span class="cm">     */</span></div><div class='line' id='LC611'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeFieldEnd</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC612'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">value</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">pop</span><span class="p">();</span></div><div class='line' id='LC613'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">fieldInfo</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">pop</span><span class="p">();</span></div><div class='line' id='LC614'><br/></div><div class='line' id='LC615'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">[</span><span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">length</span> <span class="o">-</span> <span class="mi">1</span><span class="p">][</span><span class="nx">fieldInfo</span><span class="p">.</span><span class="nx">fieldId</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;{&#39;</span> <span class="o">+</span></div><div class='line' id='LC616'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">fieldInfo</span><span class="p">.</span><span class="nx">fieldType</span> <span class="o">+</span> <span class="s1">&#39;:&#39;</span> <span class="o">+</span> <span class="nx">value</span> <span class="o">+</span> <span class="s1">&#39;}&#39;</span><span class="p">;</span></div><div class='line' id='LC617'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tpos</span><span class="p">.</span><span class="nx">pop</span><span class="p">();</span></div><div class='line' id='LC618'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC619'><br/></div><div class='line' id='LC620'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC621'><span class="cm">     * Serializes the end of the set of fields for a struct.</span></div><div class='line' id='LC622'><span class="cm">     */</span></div><div class='line' id='LC623'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeFieldStop</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC624'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="c1">//na</span></div><div class='line' id='LC625'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC626'><br/></div><div class='line' id='LC627'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC628'><span class="cm">     * Serializes the beginning of a map collection.</span></div><div class='line' id='LC629'><span class="cm">     * @param {Thrift.Type} keyType - The data type of the key.</span></div><div class='line' id='LC630'><span class="cm">     * @param {Thrift.Type} valType - The data type of the value.</span></div><div class='line' id='LC631'><span class="cm">     * @param {number} [size] - The number of elements in the map (ignored).</span></div><div class='line' id='LC632'><span class="cm">     */</span></div><div class='line' id='LC633'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeMapBegin</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">keyType</span><span class="p">,</span> <span class="nx">valType</span><span class="p">,</span> <span class="nx">size</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC634'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tpos</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">length</span><span class="p">);</span></div><div class='line' id='LC635'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">push</span><span class="p">([</span><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Type</span><span class="p">[</span><span class="nx">keyType</span><span class="p">],</span></div><div class='line' id='LC636'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Type</span><span class="p">[</span><span class="nx">valType</span><span class="p">],</span> <span class="mi">0</span><span class="p">]);</span></div><div class='line' id='LC637'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC638'><br/></div><div class='line' id='LC639'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC640'><span class="cm">     * Serializes the end of a map.</span></div><div class='line' id='LC641'><span class="cm">     */</span></div><div class='line' id='LC642'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeMapEnd</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC643'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">p</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">tpos</span><span class="p">.</span><span class="nx">pop</span><span class="p">();</span></div><div class='line' id='LC644'><br/></div><div class='line' id='LC645'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">p</span> <span class="o">==</span> <span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">length</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC646'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span><span class="p">;</span></div><div class='line' id='LC647'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC648'><br/></div><div class='line' id='LC649'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">((</span><span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">length</span> <span class="o">-</span> <span class="nx">p</span> <span class="o">-</span> <span class="mi">1</span><span class="p">)</span> <span class="o">%</span> <span class="mi">2</span> <span class="o">!==</span> <span class="mi">0</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC650'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="s1">&#39;&#39;</span><span class="p">);</span></div><div class='line' id='LC651'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC652'><br/></div><div class='line' id='LC653'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">size</span> <span class="o">=</span> <span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">length</span> <span class="o">-</span> <span class="nx">p</span> <span class="o">-</span> <span class="mi">1</span><span class="p">)</span> <span class="o">/</span> <span class="mi">2</span><span class="p">;</span></div><div class='line' id='LC654'><br/></div><div class='line' id='LC655'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">[</span><span class="nx">p</span><span class="p">][</span><span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">[</span><span class="nx">p</span><span class="p">].</span><span class="nx">length</span> <span class="o">-</span> <span class="mi">1</span><span class="p">]</span> <span class="o">=</span> <span class="nx">size</span><span class="p">;</span></div><div class='line' id='LC656'><br/></div><div class='line' id='LC657'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">map</span> <span class="o">=</span> <span class="s1">&#39;}&#39;</span><span class="p">;</span></div><div class='line' id='LC658'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">first</span> <span class="o">=</span> <span class="kc">true</span><span class="p">;</span></div><div class='line' id='LC659'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">while</span> <span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">length</span> <span class="o">&gt;</span> <span class="nx">p</span> <span class="o">+</span> <span class="mi">1</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC660'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">v</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">pop</span><span class="p">();</span></div><div class='line' id='LC661'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">k</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">pop</span><span class="p">();</span></div><div class='line' id='LC662'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">first</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC663'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">first</span> <span class="o">=</span> <span class="kc">false</span><span class="p">;</span></div><div class='line' id='LC664'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span> <span class="k">else</span> <span class="p">{</span></div><div class='line' id='LC665'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">map</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span> <span class="o">+</span> <span class="nx">map</span><span class="p">;</span></div><div class='line' id='LC666'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC667'><br/></div><div class='line' id='LC668'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="o">!</span> <span class="nb">isNaN</span><span class="p">(</span><span class="nx">k</span><span class="p">))</span> <span class="p">{</span> <span class="nx">k</span> <span class="o">=</span> <span class="s1">&#39;&quot;&#39;</span> <span class="o">+</span> <span class="nx">k</span> <span class="o">+</span> <span class="s1">&#39;&quot;&#39;</span><span class="p">;</span> <span class="p">}</span> <span class="c1">//json &quot;keys&quot; need to be strings</span></div><div class='line' id='LC669'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">map</span> <span class="o">=</span> <span class="nx">k</span> <span class="o">+</span> <span class="s1">&#39;:&#39;</span> <span class="o">+</span> <span class="nx">v</span> <span class="o">+</span> <span class="nx">map</span><span class="p">;</span></div><div class='line' id='LC670'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC671'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">map</span> <span class="o">=</span> <span class="s1">&#39;{&#39;</span> <span class="o">+</span> <span class="nx">map</span><span class="p">;</span></div><div class='line' id='LC672'><br/></div><div class='line' id='LC673'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">[</span><span class="nx">p</span><span class="p">].</span><span class="nx">push</span><span class="p">(</span><span class="nx">map</span><span class="p">);</span></div><div class='line' id='LC674'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">[</span><span class="nx">p</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;[&#39;</span> <span class="o">+</span> <span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">[</span><span class="nx">p</span><span class="p">].</span><span class="nx">join</span><span class="p">(</span><span class="s1">&#39;,&#39;</span><span class="p">)</span> <span class="o">+</span> <span class="s1">&#39;]&#39;</span><span class="p">;</span></div><div class='line' id='LC675'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC676'><br/></div><div class='line' id='LC677'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC678'><span class="cm">     * Serializes the beginning of a list collection.</span></div><div class='line' id='LC679'><span class="cm">     * @param {Thrift.Type} elemType - The data type of the elements.</span></div><div class='line' id='LC680'><span class="cm">     * @param {number} size - The number of elements in the list.</span></div><div class='line' id='LC681'><span class="cm">     */</span></div><div class='line' id='LC682'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeListBegin</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">elemType</span><span class="p">,</span> <span class="nx">size</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC683'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tpos</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">length</span><span class="p">);</span></div><div class='line' id='LC684'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">push</span><span class="p">([</span><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Type</span><span class="p">[</span><span class="nx">elemType</span><span class="p">],</span> <span class="nx">size</span><span class="p">]);</span></div><div class='line' id='LC685'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC686'><br/></div><div class='line' id='LC687'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC688'><span class="cm">     * Serializes the end of a list.</span></div><div class='line' id='LC689'><span class="cm">     */</span></div><div class='line' id='LC690'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeListEnd</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC691'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">p</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">tpos</span><span class="p">.</span><span class="nx">pop</span><span class="p">();</span></div><div class='line' id='LC692'><br/></div><div class='line' id='LC693'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">while</span> <span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">length</span> <span class="o">&gt;</span> <span class="nx">p</span> <span class="o">+</span> <span class="mi">1</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC694'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">tmpVal</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">[</span><span class="nx">p</span> <span class="o">+</span> <span class="mi">1</span><span class="p">];</span></div><div class='line' id='LC695'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">splice</span><span class="p">(</span><span class="nx">p</span> <span class="o">+</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">);</span></div><div class='line' id='LC696'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">[</span><span class="nx">p</span><span class="p">].</span><span class="nx">push</span><span class="p">(</span><span class="nx">tmpVal</span><span class="p">);</span></div><div class='line' id='LC697'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC698'><br/></div><div class='line' id='LC699'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">[</span><span class="nx">p</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;[&#39;</span> <span class="o">+</span> <span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">[</span><span class="nx">p</span><span class="p">].</span><span class="nx">join</span><span class="p">(</span><span class="s1">&#39;,&#39;</span><span class="p">)</span> <span class="o">+</span> <span class="s1">&#39;]&#39;</span><span class="p">;</span></div><div class='line' id='LC700'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC701'><br/></div><div class='line' id='LC702'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC703'><span class="cm">     * Serializes the beginning of a set collection.</span></div><div class='line' id='LC704'><span class="cm">     * @param {Thrift.Type} elemType - The data type of the elements.</span></div><div class='line' id='LC705'><span class="cm">     * @param {number} size - The number of elements in the list.</span></div><div class='line' id='LC706'><span class="cm">     */</span></div><div class='line' id='LC707'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeSetBegin</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">elemType</span><span class="p">,</span> <span class="nx">size</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC708'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tpos</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">length</span><span class="p">);</span></div><div class='line' id='LC709'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">push</span><span class="p">([</span><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Type</span><span class="p">[</span><span class="nx">elemType</span><span class="p">],</span> <span class="nx">size</span><span class="p">]);</span></div><div class='line' id='LC710'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC711'><br/></div><div class='line' id='LC712'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC713'><span class="cm">     * Serializes the end of a set.</span></div><div class='line' id='LC714'><span class="cm">     */</span></div><div class='line' id='LC715'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeSetEnd</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC716'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">p</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">tpos</span><span class="p">.</span><span class="nx">pop</span><span class="p">();</span></div><div class='line' id='LC717'><br/></div><div class='line' id='LC718'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">while</span> <span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">length</span> <span class="o">&gt;</span> <span class="nx">p</span> <span class="o">+</span> <span class="mi">1</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC719'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">tmpVal</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">[</span><span class="nx">p</span> <span class="o">+</span> <span class="mi">1</span><span class="p">];</span></div><div class='line' id='LC720'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">splice</span><span class="p">(</span><span class="nx">p</span> <span class="o">+</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">);</span></div><div class='line' id='LC721'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">[</span><span class="nx">p</span><span class="p">].</span><span class="nx">push</span><span class="p">(</span><span class="nx">tmpVal</span><span class="p">);</span></div><div class='line' id='LC722'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC723'><br/></div><div class='line' id='LC724'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">[</span><span class="nx">p</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;[&#39;</span> <span class="o">+</span> <span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">[</span><span class="nx">p</span><span class="p">].</span><span class="nx">join</span><span class="p">(</span><span class="s1">&#39;,&#39;</span><span class="p">)</span> <span class="o">+</span> <span class="s1">&#39;]&#39;</span><span class="p">;</span></div><div class='line' id='LC725'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC726'><br/></div><div class='line' id='LC727'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Serializes a boolean */</span></div><div class='line' id='LC728'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeBool</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">value</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC729'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="nx">value</span> <span class="o">?</span> <span class="mi">1</span> <span class="o">:</span> <span class="mi">0</span><span class="p">);</span></div><div class='line' id='LC730'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC731'><br/></div><div class='line' id='LC732'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Serializes a number */</span></div><div class='line' id='LC733'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeByte</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">i8</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC734'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="nx">i8</span><span class="p">);</span></div><div class='line' id='LC735'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC736'><br/></div><div class='line' id='LC737'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Serializes a number */</span></div><div class='line' id='LC738'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeI16</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">i16</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC739'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="nx">i16</span><span class="p">);</span></div><div class='line' id='LC740'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC741'><br/></div><div class='line' id='LC742'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Serializes a number */</span></div><div class='line' id='LC743'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeI32</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">i32</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC744'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="nx">i32</span><span class="p">);</span></div><div class='line' id='LC745'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC746'><br/></div><div class='line' id='LC747'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Serializes a number */</span></div><div class='line' id='LC748'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeI64</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">i64</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC749'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="nx">i64</span><span class="p">);</span></div><div class='line' id='LC750'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC751'><br/></div><div class='line' id='LC752'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Serializes a number */</span></div><div class='line' id='LC753'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeDouble</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">dbl</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC754'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="nx">dbl</span><span class="p">);</span></div><div class='line' id='LC755'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC756'><br/></div><div class='line' id='LC757'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Serializes a string */</span></div><div class='line' id='LC758'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeString</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">str</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC759'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="c1">// We do not encode uri components for wire transfer:</span></div><div class='line' id='LC760'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">str</span> <span class="o">===</span> <span class="kc">null</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC761'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="kc">null</span><span class="p">);</span></div><div class='line' id='LC762'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span> <span class="k">else</span> <span class="p">{</span></div><div class='line' id='LC763'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="c1">// concat may be slower than building a byte buffer</span></div><div class='line' id='LC764'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">escapedString</span> <span class="o">=</span> <span class="s1">&#39;&#39;</span><span class="p">;</span></div><div class='line' id='LC765'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">for</span> <span class="p">(</span><span class="kd">var</span> <span class="nx">i</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span> <span class="nx">i</span> <span class="o">&lt;</span> <span class="nx">str</span><span class="p">.</span><span class="nx">length</span><span class="p">;</span> <span class="nx">i</span><span class="o">++</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC766'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">ch</span> <span class="o">=</span> <span class="nx">str</span><span class="p">.</span><span class="nx">charAt</span><span class="p">(</span><span class="nx">i</span><span class="p">);</span>      <span class="c1">// a single double quote: &quot;</span></div><div class='line' id='LC767'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">ch</span> <span class="o">===</span> <span class="s1">&#39;\&quot;&#39;</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC768'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">escapedString</span> <span class="o">+=</span> <span class="s1">&#39;\\\&quot;&#39;</span><span class="p">;</span> <span class="c1">// write out as: \&quot;</span></div><div class='line' id='LC769'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span> <span class="k">else</span> <span class="k">if</span> <span class="p">(</span><span class="nx">ch</span> <span class="o">===</span> <span class="s1">&#39;\\&#39;</span><span class="p">)</span> <span class="p">{</span>    <span class="c1">// a single backslash: \</span></div><div class='line' id='LC770'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">escapedString</span> <span class="o">+=</span> <span class="s1">&#39;\\\\&#39;</span><span class="p">;</span> <span class="c1">// write out as: \\</span></div><div class='line' id='LC771'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/* Currently escaped forward slashes break TJSONProtocol.</span></div><div class='line' id='LC772'><span class="cm">                 * As it stands, we can simply pass forward slashes into</span></div><div class='line' id='LC773'><span class="cm">                 * our strings across the wire without being escaped.</span></div><div class='line' id='LC774'><span class="cm">                 * I think this is the protocol&#39;s bug, not thrift.js</span></div><div class='line' id='LC775'><span class="cm">                 * } else if(ch === &#39;/&#39;) {   // a single forward slash: /</span></div><div class='line' id='LC776'><span class="cm">                 *  escapedString += &#39;\\/&#39;;  // write out as \/</span></div><div class='line' id='LC777'><span class="cm">                 * }</span></div><div class='line' id='LC778'><span class="cm">                 */</span></div><div class='line' id='LC779'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span> <span class="k">else</span> <span class="k">if</span> <span class="p">(</span><span class="nx">ch</span> <span class="o">===</span> <span class="s1">&#39;\b&#39;</span><span class="p">)</span> <span class="p">{</span>    <span class="c1">// a single backspace: invisible</span></div><div class='line' id='LC780'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">escapedString</span> <span class="o">+=</span> <span class="s1">&#39;\\b&#39;</span><span class="p">;</span>  <span class="c1">// write out as: \b&quot;</span></div><div class='line' id='LC781'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span> <span class="k">else</span> <span class="k">if</span> <span class="p">(</span><span class="nx">ch</span> <span class="o">===</span> <span class="s1">&#39;\f&#39;</span><span class="p">)</span> <span class="p">{</span>    <span class="c1">// a single formfeed: invisible</span></div><div class='line' id='LC782'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">escapedString</span> <span class="o">+=</span> <span class="s1">&#39;\\f&#39;</span><span class="p">;</span>  <span class="c1">// write out as: \f&quot;</span></div><div class='line' id='LC783'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span> <span class="k">else</span> <span class="k">if</span> <span class="p">(</span><span class="nx">ch</span> <span class="o">===</span> <span class="s1">&#39;\n&#39;</span><span class="p">)</span> <span class="p">{</span>    <span class="c1">// a single newline: invisible</span></div><div class='line' id='LC784'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">escapedString</span> <span class="o">+=</span> <span class="s1">&#39;\\n&#39;</span><span class="p">;</span>  <span class="c1">// write out as: \n&quot;</span></div><div class='line' id='LC785'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span> <span class="k">else</span> <span class="k">if</span> <span class="p">(</span><span class="nx">ch</span> <span class="o">===</span> <span class="s1">&#39;\r&#39;</span><span class="p">)</span> <span class="p">{</span>    <span class="c1">// a single return: invisible</span></div><div class='line' id='LC786'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">escapedString</span> <span class="o">+=</span> <span class="s1">&#39;\\r&#39;</span><span class="p">;</span>  <span class="c1">// write out as: \r&quot;</span></div><div class='line' id='LC787'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span> <span class="k">else</span> <span class="k">if</span> <span class="p">(</span><span class="nx">ch</span> <span class="o">===</span> <span class="s1">&#39;\t&#39;</span><span class="p">)</span> <span class="p">{</span>    <span class="c1">// a single tab: invisible</span></div><div class='line' id='LC788'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">escapedString</span> <span class="o">+=</span> <span class="s1">&#39;\\t&#39;</span><span class="p">;</span>  <span class="c1">// write out as: \t&quot;</span></div><div class='line' id='LC789'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span> <span class="k">else</span> <span class="p">{</span></div><div class='line' id='LC790'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">escapedString</span> <span class="o">+=</span> <span class="nx">ch</span><span class="p">;</span>     <span class="c1">// Else it need not be escaped</span></div><div class='line' id='LC791'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC792'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC793'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">tstack</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="s1">&#39;&quot;&#39;</span> <span class="o">+</span> <span class="nx">escapedString</span> <span class="o">+</span> <span class="s1">&#39;&quot;&#39;</span><span class="p">);</span></div><div class='line' id='LC794'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC795'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC796'><br/></div><div class='line' id='LC797'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Serializes a string */</span></div><div class='line' id='LC798'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">writeBinary</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">str</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC799'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">writeString</span><span class="p">(</span><span class="nx">str</span><span class="p">);</span></div><div class='line' id='LC800'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC801'><br/></div><div class='line' id='LC802'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC803'><span class="cm">       @class</span></div><div class='line' id='LC804'><span class="cm">       @name AnonReadMessageBeginReturn</span></div><div class='line' id='LC805'><span class="cm">       @property {string} fname - The name of the service method.</span></div><div class='line' id='LC806'><span class="cm">       @property {Thrift.MessageType} mtype - The type of message call.</span></div><div class='line' id='LC807'><span class="cm">       @property {number} rseqid - The sequence number of the message (0 in Thrift RPC).</span></div><div class='line' id='LC808'><span class="cm">     */</span></div><div class='line' id='LC809'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** </span></div><div class='line' id='LC810'><span class="cm">     * Deserializes the beginning of a message. </span></div><div class='line' id='LC811'><span class="cm">     * @returns {AnonReadMessageBeginReturn}</span></div><div class='line' id='LC812'><span class="cm">     */</span></div><div class='line' id='LC813'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readMessageBegin</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC814'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rstack</span> <span class="o">=</span> <span class="p">[];</span></div><div class='line' id='LC815'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rpos</span> <span class="o">=</span> <span class="p">[];</span></div><div class='line' id='LC816'><br/></div><div class='line' id='LC817'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="k">typeof</span> <span class="nx">jQuery</span> <span class="o">!==</span> <span class="s1">&#39;undefined&#39;</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC818'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">robj</span> <span class="o">=</span> <span class="nx">jQuery</span><span class="p">.</span><span class="nx">parseJSON</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">transport</span><span class="p">.</span><span class="nx">readAll</span><span class="p">());</span></div><div class='line' id='LC819'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span> <span class="k">else</span> <span class="p">{</span></div><div class='line' id='LC820'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">robj</span> <span class="o">=</span> <span class="nb">eval</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">transport</span><span class="p">.</span><span class="nx">readAll</span><span class="p">());</span></div><div class='line' id='LC821'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC822'><br/></div><div class='line' id='LC823'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">r</span> <span class="o">=</span> <span class="p">{};</span></div><div class='line' id='LC824'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">version</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">robj</span><span class="p">.</span><span class="nx">shift</span><span class="p">();</span></div><div class='line' id='LC825'><br/></div><div class='line' id='LC826'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">version</span> <span class="o">!=</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">Version</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC827'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">throw</span> <span class="s1">&#39;Wrong thrift protocol version: &#39;</span> <span class="o">+</span> <span class="nx">version</span><span class="p">;</span></div><div class='line' id='LC828'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC829'><br/></div><div class='line' id='LC830'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">r</span><span class="p">.</span><span class="nx">fname</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">robj</span><span class="p">.</span><span class="nx">shift</span><span class="p">();</span></div><div class='line' id='LC831'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">r</span><span class="p">.</span><span class="nx">mtype</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">robj</span><span class="p">.</span><span class="nx">shift</span><span class="p">();</span></div><div class='line' id='LC832'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">r</span><span class="p">.</span><span class="nx">rseqid</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">robj</span><span class="p">.</span><span class="nx">shift</span><span class="p">();</span></div><div class='line' id='LC833'><br/></div><div class='line' id='LC834'><br/></div><div class='line' id='LC835'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="c1">//get to the main obj</span></div><div class='line' id='LC836'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">robj</span><span class="p">.</span><span class="nx">shift</span><span class="p">());</span></div><div class='line' id='LC837'><br/></div><div class='line' id='LC838'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nx">r</span><span class="p">;</span></div><div class='line' id='LC839'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC840'><br/></div><div class='line' id='LC841'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Deserializes the end of a message. */</span></div><div class='line' id='LC842'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readMessageEnd</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC843'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC844'><br/></div><div class='line' id='LC845'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** </span></div><div class='line' id='LC846'><span class="cm">     * Deserializes the beginning of a struct. </span></div><div class='line' id='LC847'><span class="cm">     * @param {string} [name] - The name of the struct (ignored)</span></div><div class='line' id='LC848'><span class="cm">     * @returns {object} - An object with an empty string fname property</span></div><div class='line' id='LC849'><span class="cm">     */</span>    </div><div class='line' id='LC850'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readStructBegin</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">name</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC851'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">r</span> <span class="o">=</span> <span class="p">{};</span></div><div class='line' id='LC852'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">r</span><span class="p">.</span><span class="nx">fname</span> <span class="o">=</span> <span class="s1">&#39;&#39;</span><span class="p">;</span></div><div class='line' id='LC853'><br/></div><div class='line' id='LC854'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="c1">//incase this is an array of structs</span></div><div class='line' id='LC855'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">[</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">length</span> <span class="o">-</span> <span class="mi">1</span><span class="p">]</span> <span class="k">instanceof</span> <span class="nb">Array</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC856'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">[</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">length</span> <span class="o">-</span> <span class="mi">1</span><span class="p">].</span><span class="nx">shift</span><span class="p">());</span></div><div class='line' id='LC857'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC858'><br/></div><div class='line' id='LC859'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nx">r</span><span class="p">;</span></div><div class='line' id='LC860'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC861'><br/></div><div class='line' id='LC862'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Deserializes the end of a struct. */</span></div><div class='line' id='LC863'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readStructEnd</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC864'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">[</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">length</span> <span class="o">-</span> <span class="mi">2</span><span class="p">]</span> <span class="k">instanceof</span> <span class="nb">Array</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC865'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">pop</span><span class="p">();</span></div><div class='line' id='LC866'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC867'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC868'><br/></div><div class='line' id='LC869'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC870'><span class="cm">       @class</span></div><div class='line' id='LC871'><span class="cm">       @name AnonReadFieldBeginReturn</span></div><div class='line' id='LC872'><span class="cm">       @property {string} fname - The name of the field (always &#39;&#39;).</span></div><div class='line' id='LC873'><span class="cm">       @property {Thrift.Type} ftype - The data type of the field.</span></div><div class='line' id='LC874'><span class="cm">       @property {number} fid - The unique identifier of the field.</span></div><div class='line' id='LC875'><span class="cm">     */</span></div><div class='line' id='LC876'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** </span></div><div class='line' id='LC877'><span class="cm">     * Deserializes the beginning of a field. </span></div><div class='line' id='LC878'><span class="cm">     * @returns {AnonReadFieldBeginReturn}</span></div><div class='line' id='LC879'><span class="cm">     */</span></div><div class='line' id='LC880'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readFieldBegin</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC881'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">r</span> <span class="o">=</span> <span class="p">{};</span></div><div class='line' id='LC882'><br/></div><div class='line' id='LC883'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">fid</span> <span class="o">=</span> <span class="o">-</span><span class="mi">1</span><span class="p">;</span></div><div class='line' id='LC884'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">ftype</span> <span class="o">=</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Type</span><span class="p">.</span><span class="nx">STOP</span><span class="p">;</span></div><div class='line' id='LC885'><br/></div><div class='line' id='LC886'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="c1">//get a fieldId</span></div><div class='line' id='LC887'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">for</span> <span class="p">(</span><span class="kd">var</span> <span class="nx">f</span> <span class="k">in</span> <span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">[</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">length</span> <span class="o">-</span> <span class="mi">1</span><span class="p">]))</span> <span class="p">{</span></div><div class='line' id='LC888'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">f</span> <span class="o">===</span> <span class="kc">null</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC889'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">continue</span><span class="p">;</span></div><div class='line' id='LC890'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC891'><br/></div><div class='line' id='LC892'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">fid</span> <span class="o">=</span> <span class="nb">parseInt</span><span class="p">(</span><span class="nx">f</span><span class="p">,</span> <span class="mi">10</span><span class="p">);</span></div><div class='line' id='LC893'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rpos</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">length</span><span class="p">);</span></div><div class='line' id='LC894'><br/></div><div class='line' id='LC895'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">field</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">[</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">length</span> <span class="o">-</span> <span class="mi">1</span><span class="p">][</span><span class="nx">fid</span><span class="p">];</span></div><div class='line' id='LC896'><br/></div><div class='line' id='LC897'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="c1">//remove so we don&#39;t see it again</span></div><div class='line' id='LC898'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">delete</span> <span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">[</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">length</span> <span class="o">-</span> <span class="mi">1</span><span class="p">][</span><span class="nx">fid</span><span class="p">];</span></div><div class='line' id='LC899'><br/></div><div class='line' id='LC900'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="nx">field</span><span class="p">);</span></div><div class='line' id='LC901'><br/></div><div class='line' id='LC902'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">break</span><span class="p">;</span></div><div class='line' id='LC903'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC904'><br/></div><div class='line' id='LC905'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">fid</span> <span class="o">!=</span> <span class="o">-</span><span class="mi">1</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC906'><br/></div><div class='line' id='LC907'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="c1">//should only be 1 of these but this is the only</span></div><div class='line' id='LC908'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="c1">//way to match a key</span></div><div class='line' id='LC909'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">for</span> <span class="p">(</span><span class="kd">var</span> <span class="nx">i</span> <span class="k">in</span> <span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">[</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">length</span> <span class="o">-</span> <span class="mi">1</span><span class="p">]))</span> <span class="p">{</span></div><div class='line' id='LC910'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">RType</span><span class="p">[</span><span class="nx">i</span><span class="p">]</span> <span class="o">===</span> <span class="kc">null</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC911'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">continue</span><span class="p">;</span></div><div class='line' id='LC912'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC913'><br/></div><div class='line' id='LC914'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">ftype</span> <span class="o">=</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">RType</span><span class="p">[</span><span class="nx">i</span><span class="p">];</span></div><div class='line' id='LC915'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">[</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">length</span> <span class="o">-</span> <span class="mi">1</span><span class="p">]</span> <span class="o">=</span></div><div class='line' id='LC916'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">[</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">length</span> <span class="o">-</span> <span class="mi">1</span><span class="p">][</span><span class="nx">i</span><span class="p">];</span></div><div class='line' id='LC917'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC918'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC919'><br/></div><div class='line' id='LC920'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">r</span><span class="p">.</span><span class="nx">fname</span> <span class="o">=</span> <span class="s1">&#39;&#39;</span><span class="p">;</span></div><div class='line' id='LC921'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">r</span><span class="p">.</span><span class="nx">ftype</span> <span class="o">=</span> <span class="nx">ftype</span><span class="p">;</span></div><div class='line' id='LC922'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">r</span><span class="p">.</span><span class="nx">fid</span> <span class="o">=</span> <span class="nx">fid</span><span class="p">;</span></div><div class='line' id='LC923'><br/></div><div class='line' id='LC924'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nx">r</span><span class="p">;</span></div><div class='line' id='LC925'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC926'><br/></div><div class='line' id='LC927'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Deserializes the end of a field. */</span></div><div class='line' id='LC928'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readFieldEnd</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC929'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">pos</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">rpos</span><span class="p">.</span><span class="nx">pop</span><span class="p">();</span></div><div class='line' id='LC930'><br/></div><div class='line' id='LC931'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="c1">//get back to the right place in the stack</span></div><div class='line' id='LC932'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">while</span> <span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">length</span> <span class="o">&gt;</span> <span class="nx">pos</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC933'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">pop</span><span class="p">();</span></div><div class='line' id='LC934'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC935'><br/></div><div class='line' id='LC936'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC937'><br/></div><div class='line' id='LC938'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC939'><span class="cm">       @class</span></div><div class='line' id='LC940'><span class="cm">       @name AnonReadMapBeginReturn</span></div><div class='line' id='LC941'><span class="cm">       @property {Thrift.Type} ktype - The data type of the key.</span></div><div class='line' id='LC942'><span class="cm">       @property {Thrift.Type} vtype - The data type of the value.</span></div><div class='line' id='LC943'><span class="cm">       @property {number} size - The number of elements in the map.</span></div><div class='line' id='LC944'><span class="cm">     */</span></div><div class='line' id='LC945'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** </span></div><div class='line' id='LC946'><span class="cm">     * Deserializes the beginning of a map. </span></div><div class='line' id='LC947'><span class="cm">     * @returns {AnonReadMapBeginReturn}</span></div><div class='line' id='LC948'><span class="cm">     */</span></div><div class='line' id='LC949'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readMapBegin</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC950'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">map</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">pop</span><span class="p">();</span></div><div class='line' id='LC951'><br/></div><div class='line' id='LC952'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">r</span> <span class="o">=</span> <span class="p">{};</span></div><div class='line' id='LC953'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">r</span><span class="p">.</span><span class="nx">ktype</span> <span class="o">=</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">RType</span><span class="p">[</span><span class="nx">map</span><span class="p">.</span><span class="nx">shift</span><span class="p">()];</span></div><div class='line' id='LC954'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">r</span><span class="p">.</span><span class="nx">vtype</span> <span class="o">=</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">RType</span><span class="p">[</span><span class="nx">map</span><span class="p">.</span><span class="nx">shift</span><span class="p">()];</span></div><div class='line' id='LC955'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">r</span><span class="p">.</span><span class="nx">size</span> <span class="o">=</span> <span class="nx">map</span><span class="p">.</span><span class="nx">shift</span><span class="p">();</span></div><div class='line' id='LC956'><br/></div><div class='line' id='LC957'><br/></div><div class='line' id='LC958'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rpos</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">length</span><span class="p">);</span></div><div class='line' id='LC959'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="nx">map</span><span class="p">.</span><span class="nx">shift</span><span class="p">());</span></div><div class='line' id='LC960'><br/></div><div class='line' id='LC961'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nx">r</span><span class="p">;</span></div><div class='line' id='LC962'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC963'><br/></div><div class='line' id='LC964'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Deserializes the end of a map. */</span></div><div class='line' id='LC965'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readMapEnd</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC966'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">readFieldEnd</span><span class="p">();</span></div><div class='line' id='LC967'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC968'><br/></div><div class='line' id='LC969'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/**</span></div><div class='line' id='LC970'><span class="cm">       @class</span></div><div class='line' id='LC971'><span class="cm">       @name AnonReadColBeginReturn</span></div><div class='line' id='LC972'><span class="cm">       @property {Thrift.Type} etype - The data type of the element.</span></div><div class='line' id='LC973'><span class="cm">       @property {number} size - The number of elements in the collection.</span></div><div class='line' id='LC974'><span class="cm">     */</span></div><div class='line' id='LC975'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** </span></div><div class='line' id='LC976'><span class="cm">     * Deserializes the beginning of a list. </span></div><div class='line' id='LC977'><span class="cm">     * @returns {AnonReadColBeginReturn}</span></div><div class='line' id='LC978'><span class="cm">     */</span></div><div class='line' id='LC979'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readListBegin</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC980'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">list</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">[</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">length</span> <span class="o">-</span> <span class="mi">1</span><span class="p">];</span></div><div class='line' id='LC981'><br/></div><div class='line' id='LC982'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">r</span> <span class="o">=</span> <span class="p">{};</span></div><div class='line' id='LC983'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">r</span><span class="p">.</span><span class="nx">etype</span> <span class="o">=</span> <span class="nx">Thrift</span><span class="p">.</span><span class="nx">Protocol</span><span class="p">.</span><span class="nx">RType</span><span class="p">[</span><span class="nx">list</span><span class="p">.</span><span class="nx">shift</span><span class="p">()];</span></div><div class='line' id='LC984'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">r</span><span class="p">.</span><span class="nx">size</span> <span class="o">=</span> <span class="nx">list</span><span class="p">.</span><span class="nx">shift</span><span class="p">();</span></div><div class='line' id='LC985'><br/></div><div class='line' id='LC986'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rpos</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">length</span><span class="p">);</span></div><div class='line' id='LC987'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="nx">list</span><span class="p">);</span></div><div class='line' id='LC988'><br/></div><div class='line' id='LC989'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nx">r</span><span class="p">;</span></div><div class='line' id='LC990'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC991'><br/></div><div class='line' id='LC992'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Deserializes the end of a list. */</span></div><div class='line' id='LC993'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readListEnd</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC994'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">readFieldEnd</span><span class="p">();</span></div><div class='line' id='LC995'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC996'><br/></div><div class='line' id='LC997'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** </span></div><div class='line' id='LC998'><span class="cm">     * Deserializes the beginning of a set. </span></div><div class='line' id='LC999'><span class="cm">     * @returns {AnonReadColBeginReturn}</span></div><div class='line' id='LC1000'><span class="cm">     */</span></div><div class='line' id='LC1001'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readSetBegin</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">elemType</span><span class="p">,</span> <span class="nx">size</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC1002'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="k">this</span><span class="p">.</span><span class="nx">readListBegin</span><span class="p">(</span><span class="nx">elemType</span><span class="p">,</span> <span class="nx">size</span><span class="p">);</span></div><div class='line' id='LC1003'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC1004'><br/></div><div class='line' id='LC1005'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Deserializes the end of a set. */</span></div><div class='line' id='LC1006'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readSetEnd</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC1007'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="k">this</span><span class="p">.</span><span class="nx">readListEnd</span><span class="p">();</span></div><div class='line' id='LC1008'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC1009'><br/></div><div class='line' id='LC1010'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Returns an object with a value property set to </span></div><div class='line' id='LC1011'><span class="cm">     *  False unless the next number in the protocol buffer </span></div><div class='line' id='LC1012'><span class="cm">     *  is 1, in which case teh value property is True */</span></div><div class='line' id='LC1013'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readBool</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC1014'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">r</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">readI32</span><span class="p">();</span></div><div class='line' id='LC1015'><br/></div><div class='line' id='LC1016'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">r</span> <span class="o">!==</span> <span class="kc">null</span> <span class="o">&amp;&amp;</span> <span class="nx">r</span><span class="p">.</span><span class="nx">value</span> <span class="o">==</span> <span class="s1">&#39;1&#39;</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC1017'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">r</span><span class="p">.</span><span class="nx">value</span> <span class="o">=</span> <span class="kc">true</span><span class="p">;</span></div><div class='line' id='LC1018'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span> <span class="k">else</span> <span class="p">{</span></div><div class='line' id='LC1019'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">r</span><span class="p">.</span><span class="nx">value</span> <span class="o">=</span> <span class="kc">false</span><span class="p">;</span></div><div class='line' id='LC1020'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC1021'><br/></div><div class='line' id='LC1022'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nx">r</span><span class="p">;</span></div><div class='line' id='LC1023'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC1024'><br/></div><div class='line' id='LC1025'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Returns the an object with a value property set to the </span></div><div class='line' id='LC1026'><span class="cm">        next value found in the protocol buffer */</span></div><div class='line' id='LC1027'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readByte</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC1028'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="k">this</span><span class="p">.</span><span class="nx">readI32</span><span class="p">();</span></div><div class='line' id='LC1029'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC1030'><br/></div><div class='line' id='LC1031'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Returns the an object with a value property set to the </span></div><div class='line' id='LC1032'><span class="cm">        next value found in the protocol buffer */</span></div><div class='line' id='LC1033'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readI16</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC1034'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="k">this</span><span class="p">.</span><span class="nx">readI32</span><span class="p">();</span></div><div class='line' id='LC1035'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC1036'><br/></div><div class='line' id='LC1037'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Returns the an object with a value property set to the </span></div><div class='line' id='LC1038'><span class="cm">        next value found in the protocol buffer */</span></div><div class='line' id='LC1039'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readI32</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">f</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC1040'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">f</span> <span class="o">===</span> <span class="kc">undefined</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC1041'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">f</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">[</span><span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">length</span> <span class="o">-</span> <span class="mi">1</span><span class="p">];</span></div><div class='line' id='LC1042'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC1043'><br/></div><div class='line' id='LC1044'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">r</span> <span class="o">=</span> <span class="p">{};</span></div><div class='line' id='LC1045'><br/></div><div class='line' id='LC1046'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">f</span> <span class="k">instanceof</span> <span class="nb">Array</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC1047'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">f</span><span class="p">.</span><span class="nx">length</span> <span class="o">===</span> <span class="mi">0</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC1048'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">r</span><span class="p">.</span><span class="nx">value</span> <span class="o">=</span> <span class="kc">undefined</span><span class="p">;</span></div><div class='line' id='LC1049'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span> <span class="k">else</span> <span class="p">{</span></div><div class='line' id='LC1050'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">r</span><span class="p">.</span><span class="nx">value</span> <span class="o">=</span> <span class="nx">f</span><span class="p">.</span><span class="nx">shift</span><span class="p">();</span></div><div class='line' id='LC1051'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC1052'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span> <span class="k">else</span> <span class="k">if</span> <span class="p">(</span><span class="nx">f</span> <span class="k">instanceof</span> <span class="nb">Object</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC1053'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">for</span> <span class="p">(</span><span class="kd">var</span> <span class="nx">i</span> <span class="k">in</span> <span class="nx">f</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC1054'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">i</span> <span class="o">===</span> <span class="kc">null</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC1055'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">continue</span><span class="p">;</span></div><div class='line' id='LC1056'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC1057'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="nx">f</span><span class="p">[</span><span class="nx">i</span><span class="p">]);</span></div><div class='line' id='LC1058'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">delete</span> <span class="nx">f</span><span class="p">[</span><span class="nx">i</span><span class="p">];</span></div><div class='line' id='LC1059'><br/></div><div class='line' id='LC1060'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">r</span><span class="p">.</span><span class="nx">value</span> <span class="o">=</span> <span class="nx">i</span><span class="p">;</span></div><div class='line' id='LC1061'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">break</span><span class="p">;</span></div><div class='line' id='LC1062'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC1063'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span> <span class="k">else</span> <span class="p">{</span></div><div class='line' id='LC1064'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">r</span><span class="p">.</span><span class="nx">value</span> <span class="o">=</span> <span class="nx">f</span><span class="p">;</span></div><div class='line' id='LC1065'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">rstack</span><span class="p">.</span><span class="nx">pop</span><span class="p">();</span></div><div class='line' id='LC1066'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC1067'><br/></div><div class='line' id='LC1068'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nx">r</span><span class="p">;</span></div><div class='line' id='LC1069'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC1070'><br/></div><div class='line' id='LC1071'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Returns the an object with a value property set to the </span></div><div class='line' id='LC1072'><span class="cm">        next value found in the protocol buffer */</span></div><div class='line' id='LC1073'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readI64</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC1074'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="k">this</span><span class="p">.</span><span class="nx">readI32</span><span class="p">();</span></div><div class='line' id='LC1075'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC1076'><br/></div><div class='line' id='LC1077'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Returns the an object with a value property set to the </span></div><div class='line' id='LC1078'><span class="cm">        next value found in the protocol buffer */</span></div><div class='line' id='LC1079'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readDouble</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC1080'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="k">this</span><span class="p">.</span><span class="nx">readI32</span><span class="p">();</span></div><div class='line' id='LC1081'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC1082'><br/></div><div class='line' id='LC1083'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Returns the an object with a value property set to the </span></div><div class='line' id='LC1084'><span class="cm">        next value found in the protocol buffer */</span></div><div class='line' id='LC1085'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readString</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC1086'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">r</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">readI32</span><span class="p">();</span></div><div class='line' id='LC1087'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nx">r</span><span class="p">;</span></div><div class='line' id='LC1088'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC1089'><br/></div><div class='line' id='LC1090'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** Returns the an object with a value property set to the </span></div><div class='line' id='LC1091'><span class="cm">        next value found in the protocol buffer */</span></div><div class='line' id='LC1092'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">readBinary</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC1093'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="k">this</span><span class="p">.</span><span class="nx">readString</span><span class="p">();</span></div><div class='line' id='LC1094'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC1095'><br/></div><div class='line' id='LC1096'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="cm">/** </span></div><div class='line' id='LC1097'><span class="cm">     * Method to arbitrarily skip over data (not implemented).</span></div><div class='line' id='LC1098'><span class="cm">     * @throws {string} this method is not implemented and always throws.</span></div><div class='line' id='LC1099'><span class="cm">     */</span></div><div class='line' id='LC1100'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">skip</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">type</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC1101'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">throw</span> <span class="s1">&#39;skip not supported yet&#39;</span><span class="p">;</span></div><div class='line' id='LC1102'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC1103'><span class="p">};</span></div></pre></div>
            </td>
          </tr>
        </table>
  </div>

  </div>
</div>

<a href="#jump-to-line" rel="facebox[.linejump]" data-hotkey="l" class="js-jump-to-line" style="display:none">Jump to Line</a>
<div id="jump-to-line" style="display:none">
  <form accept-charset="UTF-8" class="js-jump-to-line-form">
    <input class="linejump-input js-jump-to-line-field" type="text" placeholder="Jump to line&hellip;" autofocus>
    <button type="submit" class="button">Go</button>
  </form>
</div>

        </div>

      </div><!-- /.repo-container -->
      <div class="modal-backdrop"></div>
    </div><!-- /.container -->
  </div><!-- /.site -->


    </div><!-- /.wrapper -->

      <div class="container">
  <div class="site-footer">
    <ul class="site-footer-links right">
      <li><a href="https://status.github.com/">Status</a></li>
      <li><a href="http://developer.github.com">API</a></li>
      <li><a href="http://training.github.com">Training</a></li>
      <li><a href="http://shop.github.com">Shop</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="/about">About</a></li>

    </ul>

    <a href="/">
      <span class="mega-octicon octicon-mark-github"></span>
    </a>

    <ul class="site-footer-links">
      <li>&copy; 2013 <span title="0.07582s from github-fe117-cp1-prd.iad.github.net">GitHub</span>, Inc.</li>
        <li><a href="/site/terms">Terms</a></li>
        <li><a href="/site/privacy">Privacy</a></li>
        <li><a href="/security">Security</a></li>
        <li><a href="/contact">Contact</a></li>
    </ul>
  </div><!-- /.site-footer -->
</div><!-- /.container -->


    <div class="fullscreen-overlay js-fullscreen-overlay" id="fullscreen_overlay">
  <div class="fullscreen-container js-fullscreen-container">
    <div class="textarea-wrap">
      <textarea name="fullscreen-contents" id="fullscreen-contents" class="js-fullscreen-contents" placeholder="" data-suggester="fullscreen_suggester"></textarea>
          <div class="suggester-container">
              <div class="suggester fullscreen-suggester js-navigation-container" id="fullscreen_suggester"
                 data-url="/apache/thrift/suggestions/commit">
              </div>
          </div>
    </div>
  </div>
  <div class="fullscreen-sidebar">
    <a href="#" class="exit-fullscreen js-exit-fullscreen tooltipped leftwards" title="Exit Zen Mode">
      <span class="mega-octicon octicon-screen-normal"></span>
    </a>
    <a href="#" class="theme-switcher js-theme-switcher tooltipped leftwards"
      title="Switch themes">
      <span class="octicon octicon-color-mode"></span>
    </a>
  </div>
</div>



    <div id="ajax-error-message" class="flash flash-error">
      <span class="octicon octicon-alert"></span>
      <a href="#" class="octicon octicon-remove-close close ajax-error-dismiss"></a>
      Something went wrong with that request. Please try again.
    </div>

  </body>
</html>

