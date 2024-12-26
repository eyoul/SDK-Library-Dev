from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class Parameter(BaseModel):
    """Key-value parameter model"""
    Key: str
    Value: str

class ReferenceData(BaseModel):
    """Reference data model"""
    Key: str
    Value: str

class Initiator(BaseModel):
    """Initiator model for B2C transactions"""
    IdentifierType: int
    Identifier: str
    SecurityCredential: str
    SecretKey: Optional[str] = None

class Party(BaseModel):
    """Party model for transactions"""
    IdentifierType: int
    Identifier: str
    ShortCode: Optional[str] = None

class STKPushRequest(BaseModel):
    """STK Push request model"""
    MerchantRequestID: str
    BusinessShortCode: str
    Password: str
    Timestamp: str
    TransactionType: str = "CustomerPayBillOnline"
    Amount: str
    PartyA: str
    PartyB: str
    PhoneNumber: str
    TransactionDesc: str
    CallBackURL: str
    AccountReference: str
    ReferenceData: Optional[List[ReferenceData]] = None

class STKPushResponse(BaseModel):
    """STK Push response model"""
    MerchantRequestID: str
    CheckoutRequestID: str
    ResponseCode: str
    ResponseDescription: str
    CustomerMessage: str

class C2BRegisterURLRequest(BaseModel):
    """C2B URL registration request model"""
    ShortCode: str
    ResponseType: str
    CommandID: str = "RegisterURL"
    ConfirmationURL: str
    ValidationURL: str

class C2BPaymentRequest(BaseModel):
    """C2B payment request model"""
    RequestRefID: str
    CommandID: str
    Remark: str
    ChannelSessionID: str
    SourceSystem: str
    Timestamp: datetime
    Parameters: List[Parameter]
    ReferenceData: Optional[List[ReferenceData]] = None
    Initiator: Initiator
    PrimaryParty: Party
    ReceiverParty: Party

class B2CRequest(BaseModel):
    """B2C payment request model"""
    InitiatorName: str
    SecurityCredential: str
    CommandID: str = "BusinessPayment"
    Amount: int
    PartyA: str
    PartyB: str
    Remarks: str
    QueueTimeOutURL: str
    ResultURL: str
    Occassion: Optional[str] = None

class TransactionResponse(BaseModel):
    """Generic transaction response model"""
    ResponseCode: str
    ResponseDescription: str
    ConversationID: Optional[str] = None
    OriginatorConversationID: Optional[str] = None
    TransactionID: Optional[str] = None
