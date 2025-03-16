import React, { useRef } from "react";

import "./Message.css";
const Message = ({ sender, id, content, time }) => {
  return (
    <div key={id} className={`message-container  ${sender}-message`}>
      <div className="message">
        <a
          className="message-content"
          dangerouslySetInnerHTML={{ __html: content }}
        ></a>
        <a className="message-timestamp">{time}</a>
      </div>
      <div className="message-toolbar"></div>
    </div>
  );
};

export default Message;
